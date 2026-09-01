"""
Gerador de fixtures XML sintéticas para teste do parser Opera Cloud
(RES_DETAIL). Todos os dados são 100% inventados -- nunca usar informação
real de hóspede aqui. Ver docs/technical/opera-field-reference.md para a
estrutura de campos confirmada contra o relatório real.

Uso: flask generate-test-fixtures
"""

import os
import xml.etree.ElementTree as ET


def montar_comentario(comment_type: str, title: str, texto: str,
                       resv_name_id: str, order_by: int = 1) -> ET.Element:
    """
    Monta um bloco G_COMMENT_RESV_NAME_ID.

    comment_type: código cru do relatório (ex: "GEN", "RES", "CAS").
                  Tratado como opaco -- não precisa "fazer sentido" com
                  o texto, pois no arquivo real um mesmo código pode
                  cobrir mais de um tipo de nota (ver opera-field-
                  reference.md, seção sobre CAS/OCC/GIFT).
    title: vem de RES_COMMENT_DESCRIPTION. Independente do comment_type.
    texto: vem de RES_COMMENT -- o conteúdo livre da nota.
    resv_name_id: repete o identificador interno da reserva-mãe.
    order_by: valor cru do Opera (RES_COMMENT_ORDER_BY). Sabemos que é
              constante por tipo e não reflete a ordem real (decisão de
              2026-08-26) -- o parser real vai ignorar este valor e usar
              a ordem de leitura no XML. Aqui só precisamos de um valor
              plausível para o fixture não ficar com um campo vazio.
    """
    bloco = ET.Element("G_COMMENT_RESV_NAME_ID")
    ET.SubElement(bloco, "RES_COMMENT_ORDER_BY").text = str(order_by)
    ET.SubElement(bloco, "RES_COMMENT_TYPE").text = comment_type
    ET.SubElement(bloco, "RES_COMMENT").text = texto
    ET.SubElement(bloco, "RES_COMMENT_DESCRIPTION").text = title
    ET.SubElement(bloco, "COMMENT_RESV_NAME_ID").text = resv_name_id
    # CF_NOTE_DESC confirmado como espelho do title, exceto quando
    # title == "IN HOUSE" (nesse caso vem vazio no arquivo real).
    cf_valor = "" if title == "IN HOUSE" else title
    ET.SubElement(bloco, "CF_NOTE_DESC").text = cf_valor
    return bloco


def montar_dept_trace(dept_id: str, data: str, texto: str,
                       resv_name_id: str) -> ET.Element:
    """
    Monta um bloco G_DEPT_ID (trace interno).

    dept_id: código de departamento (ex: "REC", "HSK") -- ver lista
             completa em opera-field-reference.md.
    data: formato DD/MM/AA, mesma convenção de ARRIVAL/DEPARTURE.
    texto: conteúdo livre do trace (TRACE_TEXT).
    """
    bloco = ET.Element("G_DEPT_ID")
    ET.SubElement(bloco, "GTV_TRACE_ON").text = data
    ET.SubElement(bloco, "RESV_NAME_ID1").text = resv_name_id
    ET.SubElement(bloco, "DEPT_ID").text = dept_id
    ET.SubElement(bloco, "TRACE_TEXT").text = texto
    return bloco


def montar_membership(tipo: str, resv_name_id: str) -> ET.Element:
    """
    Monta um bloco G_MEM_TYPE_LEVEL (nível de fidelidade ALL).

    tipo: valor de MEMBERSHIP_TYPE (ex: "A3", "A6", "ID", "G7").
          Tipos fora de A1-A6 devem ser totalmente ignorados pelo
          parser (decisão de 2026-08-16) -- por isso o fixture
          também vai incluir tipos "ID"/"G7" de propósito, para
          testar que são mesmo ignorados.
    """
    bloco = ET.Element("G_MEM_TYPE_LEVEL")
    ET.SubElement(bloco, "RESV_NAME_ID1").text = resv_name_id
    ET.SubElement(bloco, "MEMBERSHIP_TYPE").text = tipo
    # MEMBERSHIP_LEVEL confirmado como sempre vazio no arquivo real
    # (decisão de 2026-08-26) -- reproduzimos esse comportamento aqui.
    ET.SubElement(bloco, "MEMBERSHIP_LEVEL").text = ""
    return bloco


def montar_reserva(
    confirmation_no: str,
    guest_name_id: str,
    full_name: str,
    arrival: str,
    departure: str,
    trunc_begin: str,
    trunc_end: str,
    room_no: str = "",
    is_shared: bool = False,
    adults: int = 1,
    children: int = 0,
    short_resv_status: str = "GRD",
    membership_types: list[str] | None = None,
    rate_code: str = "",
    comments: list[dict] | None = None,
    dept_traces: list[dict] | None = None,
) -> ET.Element:
    """
    Monta um bloco G_RESERVATION completo.

    arrival/departure: formato DD/MM/AA (ex: "05/09/26").
    trunc_begin/trunc_end: formato DD-MON-AA (ex: "05-SEP-26"). Devem
                            bater com arrival/departure -- exceto no
                            cenário proposital de divergência (que
                            testa o envio para ImportErrorRecord).
    membership_types: lista de strings, ex: ["A3", "A6"]. Vazia por
                       padrão (hóspede sem fidelidade).
    comments: lista de dicts, cada um com as chaves esperadas por
              montar_comentario (comment_type, title, texto, order_by).
    dept_traces: lista de dicts, cada um com as chaves esperadas por
                 montar_dept_trace (dept_id, data, texto).
    """
    if membership_types is None:
        membership_types = []
    if comments is None:
        comments = []
    if dept_traces is None:
        dept_traces = []

    resv = ET.Element("G_RESERVATION")
    ET.SubElement(resv, "CONFIRMATION_NO").text = confirmation_no
    ET.SubElement(resv, "GUEST_NAME_ID").text = guest_name_id
    ET.SubElement(resv, "FULL_NAME").text = full_name
    ET.SubElement(resv, "ARRIVAL").text = arrival
    ET.SubElement(resv, "DEPARTURE").text = departure
    ET.SubElement(resv, "TRUNC_BEGIN").text = trunc_begin
    ET.SubElement(resv, "TRUNC_END").text = trunc_end
    ET.SubElement(resv, "ROOM_NO").text = room_no
    ET.SubElement(resv, "IS_SHARED_YN").text = "Y" if is_shared else "N"
    ET.SubElement(resv, "ADULTS").text = str(adults)
    ET.SubElement(resv, "CHILDREN").text = str(children)
    ET.SubElement(resv, "SHORT_RESV_STATUS").text = short_resv_status
    ET.SubElement(resv, "RATE_CODE").text = rate_code

    # LIST_G_MEM_TYPE_LEVEL -- sempre presente, mesmo vazio (convenção
    # confirmada em 2026-08-26: contêiner aparece mesmo sem itens).
    lista_membership = ET.SubElement(resv, "LIST_G_MEM_TYPE_LEVEL")
    for tipo in membership_types:
        lista_membership.append(montar_membership(tipo, confirmation_no))

    # LIST_G_COMMENT_RESV_NAME_ID
    lista_comentarios = ET.SubElement(resv, "LIST_G_COMMENT_RESV_NAME_ID")
    for c in comments:
        lista_comentarios.append(montar_comentario(
            comment_type=c["comment_type"],
            title=c["title"],
            texto=c["texto"],
            resv_name_id=confirmation_no,
            order_by=c.get("order_by", 1),
        ))

    # LIST_G_DEPT_ID
    lista_traces = ET.SubElement(resv, "LIST_G_DEPT_ID")
    for t in dept_traces:
        lista_traces.append(montar_dept_trace(
            dept_id=t["dept_id"],
            data=t["data"],
            texto=t["texto"],
            resv_name_id=confirmation_no,
        ))

    return resv


def distribuir_em_grupos(reservas: list[ET.Element],
                          tamanhos: list[int]) -> list[list[ET.Element]]:
    """
    Separa a lista de reservas em grupos (representando os múltiplos
    G_GROUP_BY1 do relatório real -- decisão de 2026-08-26: o parser
    real precisa iterar todos os grupos, nunca só o primeiro).

    tamanhos: quantas reservas cada grupo deve ter, ex: [1, 2, 7].
              A soma DEVE bater exatamente com len(reservas), ou a
              função levanta erro -- preferimos falhar alto a perder
              uma reserva silenciosamente num grupo errado.
    """
    if sum(tamanhos) != len(reservas):
        raise ValueError(
            f"Soma dos tamanhos ({sum(tamanhos)}) não bate com o "
            f"número de reservas ({len(reservas)})."
        )
    grupos = []
    indice = 0
    for tamanho in tamanhos:
        grupos.append(reservas[indice:indice + tamanho])
        indice += tamanho
    return grupos


def montar_xml_completo(grupos: list[list[ET.Element]]) -> ET.Element:
    """
    Monta a estrutura completa: RES_DETAIL > LIST_G_GROUP_BY1 >
    (um G_GROUP_BY1 por grupo) > LIST_G_RESERVATION > reservas.
    """
    raiz = ET.Element("RES_DETAIL")
    lista_grupos = ET.SubElement(raiz, "LIST_G_GROUP_BY1")
    for grupo in grupos:
        bloco_grupo = ET.SubElement(lista_grupos, "G_GROUP_BY1")
        lista_reservas = ET.SubElement(bloco_grupo, "LIST_G_RESERVATION")
        for reserva in grupo:
            lista_reservas.append(reserva)
    return raiz


def run() -> tuple[list[str], int]:
    """
    Gera o(s) arquivo(s) de fixture em tests/fixtures/.

    VERSÃO ATUAL: só um conjunto pequeno de 3 reservas de exemplo, para
    testar o mecanismo completo (montagem + gravação + comando flask)
    antes de expandir para os 28 cenários combinados. Será substituída
    na próxima etapa.
    """
    reservas = [
        montar_reserva(
            confirmation_no="TESTE0001",
            guest_name_id="G0001",
            full_name="TESTE, HOSPEDE 01",
            arrival="05/09/26",
            departure="08/09/26",
            trunc_begin="05-SEP-26",
            trunc_end="08-SEP-26",
            room_no="101",
        ),
        montar_reserva(
            confirmation_no="TESTE0002",
            guest_name_id="G0002",
            full_name="TESTE, HOSPEDE 02",
            arrival="06/09/26",
            departure="09/09/26",
            trunc_begin="06-SEP-26",
            trunc_end="09-SEP-26",
            room_no="102",
            membership_types=["A3"],
            comments=[{
                "comment_type": "CAS",
                "title": "GENERAL",
                "texto": "Exemplo de comentario tipo CAS (teste de campo opaco).",
            }],
        ),
        montar_reserva(
            confirmation_no="TESTE0003",
            guest_name_id="G0003",
            full_name="TESTE, HOSPEDE 03",
            arrival="07/09/26",
            departure="10/09/26",
            trunc_begin="07-SEP-26",
            trunc_end="10-SEP-26",
            room_no="",
            dept_traces=[{
                "dept_id": "REC",
                "data": "06/09/26",
                "texto": "Trace de teste.",
            }],
        ),
    ]

    grupos = distribuir_em_grupos(reservas, tamanhos=[1, 2])
    raiz = montar_xml_completo(grupos)

    ET.indent(raiz, space="  ")
    arvore = ET.ElementTree(raiz)

    caminho = os.path.join("tests", "fixtures", "res_detail_sintetico.xml")
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    arvore.write(caminho, encoding="utf-8", xml_declaration=True)

    return [caminho], len(reservas)
