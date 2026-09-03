"""
Parser puro do relatorio RES_DETAIL do Opera Cloud (Frente 3, Fatia 1).

Responsabilidade unica: ler um arquivo XML no formato RES_DETAIL e devolver
estruturas de dados Python (dataclasses) com os valores CRUS extraidos.

O QUE ESTE MODULO NAO FAZ (de proposito):
- Nao toca no banco de dados (nenhum import de app.models, app.extensions).
- Nao converte datas para o tipo `date` do Python -- as datas ficam como
  string, exatamente como vem no XML (decisao de 2026-08-26: a comparacao
  entre TRUNC_BEGIN/END e ARRIVAL/DEPARTURE, e a decisao do que vira erro,
  pertencem a camada de upsert, nao ao parser).
- Nao decide status/badges/categorias -- isso e Fatia 4/5.
- Nao filtra reservas canceladas nem aplica nenhuma regra de negocio.

Trata RES_COMMENT_TYPE como campo opaco (decisao de 2026-08-12, reforcada
em 2026-08-28): nunca tenta traduzir o codigo para o tipo mostrado na
interface do Opera.
"""

from dataclasses import dataclass, field
import xml.etree.ElementTree as ET


@dataclass
class ComentarioParseado:
    comment_type: str
    title: str | None
    text: str
    order_by: int  # ordem de LEITURA no XML -- nunca o RES_COMMENT_ORDER_BY do Opera


@dataclass
class TraceParseado:
    dept_id: str
    data: str  # GTV_TRACE_ON, formato DD/MM/AA, cru
    texto: str


@dataclass
class MembershipParseado:
    membership_type: str  # ex: "A3", "ID", "G7" -- cru, sem filtro aqui
    membership_card_no: str | None


@dataclass
class ReservaParseada:
    reservation_code: str  # CONFIRMATION_NO
    full_name: str  # ja sem o prefixo "*" de share
    is_shared: bool
    opera_guest_id: str | None  # GUEST_NAME_ID
    room_number: str | None  # ROOM_NO, None quando vazio (nunca "")
    check_in: str  # TRUNC_BEGIN, cru
    check_out: str  # TRUNC_END, cru
    arrival_check: str  # ARRIVAL, para dupla verificacao (decisao 2026-08-26)
    departure_check: str  # DEPARTURE, para dupla verificacao
    opera_status: str | None  # SHORT_RESV_STATUS, cru
    adults: int | None
    children: int | None
    rate_code: str | None
    memberships: list[MembershipParseado] = field(default_factory=list)
    comments: list[ComentarioParseado] = field(default_factory=list)
    traces: list[TraceParseado] = field(default_factory=list)


def _texto(elemento, tag: str) -> str | None:
    """Busca uma tag filha direta e devolve seu texto, ou None se vazia/ausente."""
    filho = elemento.find(tag)
    if filho is None or filho.text is None:
        return None
    valor = filho.text.strip()
    return valor if valor else None


def _inteiro(elemento, tag: str) -> int | None:
    valor = _texto(elemento, tag)
    if valor is None:
        return None
    try:
        return int(valor)
    except ValueError:
        return None


def _parse_memberships(g_reservation) -> list[MembershipParseado]:
    resultado: list[MembershipParseado] = []
    lista = g_reservation.find("LIST_G_MEM_TYPE_LEVEL")
    if lista is None:
        return resultado
    for item in lista.findall("G_MEM_TYPE_LEVEL"):
        tipo = _texto(item, "MEMBERSHIP_TYPE")
        if tipo is None:
            continue
        resultado.append(
            MembershipParseado(
                membership_type=tipo,
                membership_card_no=_texto(item, "MEMBERSHIP_CARD_NO"),
            )
        )
    return resultado


def _parse_comments(g_reservation) -> list[ComentarioParseado]:
    resultado: list[ComentarioParseado] = []
    lista = g_reservation.find("LIST_G_COMMENT_RESV_NAME_ID")
    if lista is None:
        return resultado
    ordem = 0
    for item in lista.findall("G_COMMENT_RESV_NAME_ID"):
        texto = _texto(item, "RES_COMMENT")
        if texto is None:
            continue
        ordem += 1
        resultado.append(
            ComentarioParseado(
                comment_type=_texto(item, "RES_COMMENT_TYPE") or "",
                title=_texto(item, "RES_COMMENT_DESCRIPTION"),
                text=texto,
                order_by=ordem,
            )
        )
    return resultado


def _parse_traces(g_reservation) -> list[TraceParseado]:
    resultado: list[TraceParseado] = []
    lista = g_reservation.find("LIST_G_DEPT_ID")
    if lista is None:
        return resultado
    for item in lista.findall("G_DEPT_ID"):
        dept_id = _texto(item, "DEPT_ID")
        texto = _texto(item, "TRACE_TEXT")
        if dept_id is None or texto is None:
            continue
        resultado.append(
            TraceParseado(
                dept_id=dept_id,
                data=_texto(item, "GTV_TRACE_ON") or "",
                texto=texto,
            )
        )
    return resultado


def _parse_reservation(g_reservation) -> ReservaParseada | None:
    """Extrai uma ReservaParseada de um elemento <G_RESERVATION>.

    Devolve None se algum campo OBRIGATORIO estiver ausente -- quem chama
    (parse_res_detail) decide o que fazer com isso (acumula como erro).
    """
    reservation_code = _texto(g_reservation, "CONFIRMATION_NO")
    full_name_cru = _texto(g_reservation, "FULL_NAME")
    check_in = _texto(g_reservation, "TRUNC_BEGIN")
    check_out = _texto(g_reservation, "TRUNC_END")
    arrival_check = _texto(g_reservation, "ARRIVAL")
    departure_check = _texto(g_reservation, "DEPARTURE")

    campos_obrigatorios = [
        reservation_code, full_name_cru, check_in,
        check_out, arrival_check, departure_check,
    ]
    if not all(campos_obrigatorios):
        return None

    is_shared = _texto(g_reservation, "IS_SHARED_YN") == "Y"
    full_name = full_name_cru.lstrip("*")

    return ReservaParseada(
        reservation_code=reservation_code,
        full_name=full_name,
        is_shared=is_shared,
        opera_guest_id=_texto(g_reservation, "GUEST_NAME_ID"),
        room_number=_texto(g_reservation, "ROOM_NO"),
        check_in=check_in,
        check_out=check_out,
        arrival_check=arrival_check,
        departure_check=departure_check,
        opera_status=_texto(g_reservation, "SHORT_RESV_STATUS"),
        adults=_inteiro(g_reservation, "ADULTS"),
        children=_inteiro(g_reservation, "CHILDREN"),
        rate_code=_texto(g_reservation, "RATE_CODE"),
        memberships=_parse_memberships(g_reservation),
        comments=_parse_comments(g_reservation),
        traces=_parse_traces(g_reservation),
    )


def parse_res_detail(caminho_do_arquivo: str) -> tuple[list[ReservaParseada], list[str]]:
    """
    Le um arquivo RES_DETAIL (XML do Opera Cloud) e devolve:
    - lista de ReservaParseada com sucesso
    - lista de mensagens de erro (uma por reserva que nao pode ser parseada)

    Percorre TODOS os <G_GROUP_BY1> (o relatorio e agrupado por data de
    chegada -- decisao de 2026-08-26 alerta que ler so o primeiro grupo
    importaria uma fracao das reservas sem gerar erro nenhum).
    """
    arvore = ET.parse(caminho_do_arquivo)
    raiz = arvore.getroot()

    reservas: list[ReservaParseada] = []
    erros: list[str] = []

    lista_grupos = raiz.find("LIST_G_GROUP_BY1")
    if lista_grupos is None:
        erros.append("Tag LIST_G_GROUP_BY1 nao encontrada no arquivo.")
        return reservas, erros

    for grupo in lista_grupos.findall("G_GROUP_BY1"):
        lista_reservas = grupo.find("LIST_G_RESERVATION")
        if lista_reservas is None:
            continue
        for g_reservation in lista_reservas.findall("G_RESERVATION"):
            reserva = _parse_reservation(g_reservation)
            if reserva is None:
                confirmation_no = _texto(g_reservation, "CONFIRMATION_NO") or "desconhecido"
                erros.append(
                    f"Reserva com CONFIRMATION_NO={confirmation_no}: "
                    f"campo obrigatorio ausente (CONFIRMATION_NO, FULL_NAME, "
                    f"TRUNC_BEGIN, TRUNC_END, ARRIVAL ou DEPARTURE)."
                )
                continue
            reservas.append(reserva)

    return reservas, erros