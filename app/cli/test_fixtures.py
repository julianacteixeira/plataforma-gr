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
          também inclui tipos "ID"/"G7" de propósito, para testar
          que são mesmo ignorados.
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


# ---------------------------------------------------------------------
# Cenários 1-10 (dos 28 combinados). Cada dict é passado como **kwargs
# para montar_reserva.
# ---------------------------------------------------------------------

CENARIOS_BLOCO_1 = [
    # 24: reserva comum, sem nenhum caso-limite -- controle-base.
    dict(
        confirmation_no="TESTE0001", guest_name_id="G0001",
        full_name="TESTE, HOSPEDE 01",
        arrival="05/09/26", departure="08/09/26",
        trunc_begin="05-SEP-26", trunc_end="08-SEP-26",
        room_no="101",
    ),
    # 2: ROOM_NO vazio -- quarto ainda não atribuído.
    dict(
        confirmation_no="TESTE0002", guest_name_id="G0002",
        full_name="TESTE, HOSPEDE 02",
        arrival="05/09/26", departure="07/09/26",
        trunc_begin="05-SEP-26", trunc_end="07-SEP-26",
        room_no="",
    ),
    # 8: SHORT_RESV_STATUS = CXL (cancelada, nunca apagada, só marcada).
    dict(
        confirmation_no="TESTE0003", guest_name_id="G0003",
        full_name="TESTE, HOSPEDE 03",
        arrival="10/09/26", departure="12/09/26",
        trunc_begin="10-SEP-26", trunc_end="12-SEP-26",
        room_no="103", short_resv_status="CXL",
    ),
    # 9: SHORT_RESV_STATUS = CKIN (hóspede já em check-in).
    dict(
        confirmation_no="TESTE0004", guest_name_id="G0004",
        full_name="TESTE, HOSPEDE 04",
        arrival="01/09/26", departure="06/09/26",
        trunc_begin="01-SEP-26", trunc_end="06-SEP-26",
        room_no="104", short_resv_status="CKIN",
    ),
    # 10: código de status desconhecido -- nunca deve interromper a
    # importação; deve cair em "ativa" com o valor cru visível.
    dict(
        confirmation_no="TESTE0005", guest_name_id="G0005",
        full_name="TESTE, HOSPEDE 05",
        arrival="11/09/26", departure="13/09/26",
        trunc_begin="11-SEP-26", trunc_end="13-SEP-26",
        room_no="105", short_resv_status="ZZZ",
    ),
    # 11: hóspede com 3 níveis de fidelidade diferentes na mesma
    # reserva, incluindo A6 (Limitless) -- testa "pega o nível mais
    # alto" mesmo com A6 no meio da lista, não só no fim.
    dict(
        confirmation_no="TESTE0006", guest_name_id="G0006",
        full_name="TESTE, HOSPEDE 06",
        arrival="14/09/26", departure="16/09/26",
        trunc_begin="14-SEP-26", trunc_end="16-SEP-26",
        room_no="106", membership_types=["A1", "A6", "A3"],
    ),
    # 12: MEMBERSHIP_TYPE fora da faixa A1-A6 (ID e G7) -- devem ser
    # totalmente ignorados, nem para all_member.
    dict(
        confirmation_no="TESTE0007", guest_name_id="G0007",
        full_name="TESTE, HOSPEDE 07",
        arrival="15/09/26", departure="17/09/26",
        trunc_begin="15-SEP-26", trunc_end="17-SEP-26",
        room_no="107", membership_types=["ID", "G7"],
    ),
    # 13: A1/A2 -- all_member=True, mas SEM badge automático de tier.
    dict(
        confirmation_no="TESTE0008", guest_name_id="G0008",
        full_name="TESTE, HOSPEDE 08",
        arrival="16/09/26", departure="18/09/26",
        trunc_begin="16-SEP-26", trunc_end="18-SEP-26",
        room_no="108", membership_types=["A1"],
    ),
    # 14: RATE_CODE = ALSIG1 (ALL Signature Zen Day).
    dict(
        confirmation_no="TESTE0009", guest_name_id="G0009",
        full_name="TESTE, HOSPEDE 09",
        arrival="17/09/26", departure="19/09/26",
        trunc_begin="17-SEP-26", trunc_end="19-SEP-26",
        room_no="109", rate_code="ALSIG1",
    ),
    # 14: RATE_CODE = ALSIG2 (ALL Signature Fondue).
    dict(
        confirmation_no="TESTE0010", guest_name_id="G0010",
        full_name="TESTE, HOSPEDE 10",
        arrival="18/09/26", departure="20/09/26",
        trunc_begin="18-SEP-26", trunc_end="20-SEP-26",
        room_no="110", rate_code="ALSIG2",
    ),
]


# ---------------------------------------------------------------------
# Cenários 3-7 (share de quarto). Todas usam IS_SHARED_YN=True.
# ---------------------------------------------------------------------

CENARIOS_BLOCO_2 = [
    # 3 + 7 (combinados): share de 2 reservas, MESMO quarto, datas de
    # chegada DIFERENTES (não exigir datas iguais -- decisão de
    # 2026-08-26). Uma das duas tem o prefixo "*" no FULL_NAME, que o
    # parser real deve remover. Âncora esperada: TESTE0011 (adults=2,
    # maior soma individual que TESTE0012 com adults=1).
    dict(
        confirmation_no="TESTE0011", guest_name_id="G0011",
        full_name="TESTE, HOSPEDE 11",
        arrival="05/09/26", departure="09/09/26",
        trunc_begin="05-SEP-26", trunc_end="09-SEP-26",
        room_no="201", is_shared=True, adults=2,
    ),
    dict(
        confirmation_no="TESTE0012", guest_name_id="G0012",
        full_name="*TESTE, HOSPEDE 12",  # prefixo "*" proposital
        arrival="06/09/26", departure="08/09/26",
        trunc_begin="06-SEP-26", trunc_end="08-SEP-26",
        room_no="201", is_shared=True, adults=1,
    ),

    # 4a: grupo de 3 reservas dividindo o mesmo quarto -- confirma que
    # o desenho trata "lista de irmãs", nunca um par fixo. Âncora
    # esperada: TESTE0013 (adults=2, maior valor individual do grupo).
    dict(
        confirmation_no="TESTE0013", guest_name_id="G0013",
        full_name="TESTE, HOSPEDE 13",
        arrival="10/09/26", departure="14/09/26",
        trunc_begin="10-SEP-26", trunc_end="14-SEP-26",
        room_no="202", is_shared=True, adults=2,
    ),
    dict(
        confirmation_no="TESTE0014", guest_name_id="G0014",
        full_name="TESTE, HOSPEDE 14",
        arrival="10/09/26", departure="14/09/26",
        trunc_begin="10-SEP-26", trunc_end="14-SEP-26",
        room_no="202", is_shared=True, adults=1,
    ),
    dict(
        confirmation_no="TESTE0015", guest_name_id="G0015",
        full_name="TESTE, HOSPEDE 15",
        arrival="11/09/26", departure="13/09/26",
        trunc_begin="11-SEP-26", trunc_end="13-SEP-26",
        room_no="202", is_shared=True, adults=1,
    ),

    # 4b: grupo de 4 reservas dividindo o mesmo quarto. Âncora
    # esperada: TESTE0016 (adults=2, maior valor individual).
    dict(
        confirmation_no="TESTE0016", guest_name_id="G0016",
        full_name="TESTE, HOSPEDE 16",
        arrival="15/09/26", departure="20/09/26",
        trunc_begin="15-SEP-26", trunc_end="20-SEP-26",
        room_no="203", is_shared=True, adults=2,
    ),
    dict(
        confirmation_no="TESTE0017", guest_name_id="G0017",
        full_name="TESTE, HOSPEDE 17",
        arrival="15/09/26", departure="18/09/26",
        trunc_begin="15-SEP-26", trunc_end="18-SEP-26",
        room_no="203", is_shared=True, adults=1,
    ),
    dict(
        confirmation_no="TESTE0018", guest_name_id="G0018",
        full_name="TESTE, HOSPEDE 18",
        arrival="16/09/26", departure="19/09/26",
        trunc_begin="16-SEP-26", trunc_end="19-SEP-26",
        room_no="203", is_shared=True, adults=1,
    ),
    dict(
        confirmation_no="TESTE0019", guest_name_id="G0019",
        full_name="TESTE, HOSPEDE 19",
        arrival="17/09/26", departure="20/09/26",
        trunc_begin="17-SEP-26", trunc_end="20-SEP-26",
        room_no="203", is_shared=True, adults=1,
    ),

    # 5: share onde ROOM_NO está vazio nas duas reservas -- sem vínculo
    # até o quarto ser definido numa importação posterior; não pode
    # gerar erro.
    dict(
        confirmation_no="TESTE0020", guest_name_id="G0020",
        full_name="TESTE, HOSPEDE 20",
        arrival="21/09/26", departure="23/09/26",
        trunc_begin="21-SEP-26", trunc_end="23-SEP-26",
        room_no="", is_shared=True, adults=1,
    ),
    dict(
        confirmation_no="TESTE0021", guest_name_id="G0021",
        full_name="TESTE, HOSPEDE 21",
        arrival="21/09/26", departure="23/09/26",
        trunc_begin="21-SEP-26", trunc_end="23-SEP-26",
        room_no="", is_shared=True, adults=1,
    ),

    # 6: grupo onde NENHUMA reserva tem adults>0 -- testa o desempate
    # por reservation_code (menor vence). Âncora esperada: TESTE0022
    # (código menor que TESTE0023, já que a soma de pax empata em 0).
    dict(
        confirmation_no="TESTE0022", guest_name_id="G0022",
        full_name="TESTE, HOSPEDE 22",
        arrival="24/09/26", departure="26/09/26",
        trunc_begin="24-SEP-26", trunc_end="26-SEP-26",
        room_no="204", is_shared=True, adults=0, children=0,
    ),
    dict(
        confirmation_no="TESTE0023", guest_name_id="G0023",
        full_name="TESTE, HOSPEDE 23",
        arrival="24/09/26", departure="26/09/26",
        trunc_begin="24-SEP-26", trunc_end="26-SEP-26",
        room_no="204", is_shared=True, adults=0, children=0,
    ),
]


# ---------------------------------------------------------------------
# Cenários 15-22 e 25 (últimos dos 28 combinados).
# ---------------------------------------------------------------------

CENARIOS_BLOCO_3 = [
    # 14 (conclusão): RATE_CODE = ALSIG3 (ALL Signature ALL Kids).
    dict(
        confirmation_no="TESTE0024", guest_name_id="G0024",
        full_name="TESTE, HOSPEDE 24",
        arrival="27/09/26", departure="29/09/26",
        trunc_begin="27-SEP-26", trunc_end="29-SEP-26",
        room_no="301", rate_code="ALSIG3",
    ),
    # 15: RATE_CODE = ACO (Colaboradores Accor) -- badge sempre
    # "suggested", nunca "active" (não exclusivo, decisão 2026-08-12).
    dict(
        confirmation_no="TESTE0025", guest_name_id="G0025",
        full_name="TESTE, HOSPEDE 25",
        arrival="28/09/26", departure="30/09/26",
        trunc_begin="28-SEP-26", trunc_end="30-SEP-26",
        room_no="302", rate_code="ACO",
    ),

    # 17: keyword genérica ("vip") e específica ("aniversário") na
    # mesma nota -- a específica deve vencer a disputa de categoria.
    dict(
        confirmation_no="TESTE0026", guest_name_id="G0026",
        full_name="TESTE, HOSPEDE 26",
        arrival="01/10/26", departure="03/10/26",
        trunc_begin="01-OCT-26", trunc_end="03-OCT-26",
        room_no="303",
        comments=[{
            "comment_type": "GEN", "title": "GENERAL",
            "texto": "Aniversario da hospede dia 02/10 - prever vip simbolico",
        }],
    ),

    # 18: combinação "E" (termo1+termo2) -- "pax+querido" precisa dos
    # dois termos no texto, em qualquer ordem.
    dict(
        confirmation_no="TESTE0027", guest_name_id="G0027",
        full_name="TESTE, HOSPEDE 27",
        arrival="02/10/26", departure="04/10/26",
        trunc_begin="02-OCT-26", trunc_end="04-OCT-26",
        room_no="304",
        comments=[{
            "comment_type": "RES", "title": "RESERVATION",
            "texto": "Pax querido da equipe, favor atencao especial.",
        }],
    ),

    # 16: múltiplos comentários do MESMO comment_type -- testa que
    # order_by vira sequência de leitura (1, 2, 3...), não o valor cru
    # do Opera (que é constante por tipo, decisão 2026-08-26).
    dict(
        confirmation_no="TESTE0028", guest_name_id="G0028",
        full_name="TESTE, HOSPEDE 28",
        arrival="03/10/26", departure="05/10/26",
        trunc_begin="03-OCT-26", trunc_end="05-OCT-26",
        room_no="305",
        comments=[
            {"comment_type": "GEN", "title": "GENERAL",
             "texto": "Primeira nota generica de teste.", "order_by": 1},
            {"comment_type": "GEN", "title": "GENERAL",
             "texto": "Segunda nota generica de teste.", "order_by": 1},
        ],
    ),

    # 19: normal -- ARRIVAL/DEPARTURE coerentes com TRUNC_BEGIN/END,
    # controle de comparação com o cenário 20, abaixo.
    dict(
        confirmation_no="TESTE0029", guest_name_id="G0029",
        full_name="TESTE, HOSPEDE 29",
        arrival="04/10/26", departure="06/10/26",
        trunc_begin="04-OCT-26", trunc_end="06-OCT-26",
        room_no="306",
    ),
    # 20: ARRIVAL/DEPARTURE DIVERGENTES de TRUNC_BEGIN/END -- deve ir
    # para ImportErrorRecord, sem interromper a importação das demais
    # (Opção B, erro por reserva). NOTA: este fixture só cria a
    # condição -- a lógica de detecção ainda não existe (Fatia 1).
    dict(
        confirmation_no="TESTE0030", guest_name_id="G0030",
        full_name="TESTE, HOSPEDE 30",
        arrival="05/10/26", departure="07/10/26",
        trunc_begin="20-OCT-26", trunc_end="22-OCT-26",  # proposital
        room_no="307",
    ),

    # 21: sem NENHUM G_DEPT_ID -- dept_traces deve ficar None, nunca
    # parágrafo vazio.
    dict(
        confirmation_no="TESTE0031", guest_name_id="G0031",
        full_name="TESTE, HOSPEDE 31",
        arrival="06/10/26", departure="08/10/26",
        trunc_begin="06-OCT-26", trunc_end="08-OCT-26",
        room_no="308",
    ),
    # 22: COM 2 traces -- testa formatação de múltiplos parágrafos.
    dict(
        confirmation_no="TESTE0032", guest_name_id="G0032",
        full_name="TESTE, HOSPEDE 32",
        arrival="07/10/26", departure="09/10/26",
        trunc_begin="07-OCT-26", trunc_end="09-OCT-26",
        room_no="309",
        dept_traces=[
            {"dept_id": "REC", "data": "06/10/26",
             "texto": "Primeiro trace de teste."},
            {"dept_id": "HSK", "data": "07/10/26",
             "texto": "Segundo trace de teste."},
        ],
    ),

    # 25a: mesmo GUEST_NAME_ID em 2 reservas SOBREPOSTAS, quartos
    # diferentes, NAO share. As duas devem gerar StayBadge
    # independente; juntas contam como 1 periodo de stay_count (datas
    # se sobrepõem).
    dict(
        confirmation_no="TESTE0033", guest_name_id="G0033",
        full_name="TITULAR, TESTE 33",
        arrival="10/10/26", departure="14/10/26",
        trunc_begin="10-OCT-26", trunc_end="14-OCT-26",
        room_no="401",
    ),
    dict(
        confirmation_no="TESTE0034", guest_name_id="G0033",  # mesmo hóspede
        full_name="CONVIDADO 01, TESTE 33",
        arrival="11/10/26", departure="13/10/26",
        trunc_begin="11-OCT-26", trunc_end="13-OCT-26",
        room_no="402",
    ),

    # 25b: mesmo GUEST_NAME_ID, reservas CONSECUTIVAS com gap zero
    # (checkout de uma = checkin da outra, mesmo dia) -- devem fundir
    # em 1 periodo, nao 2.
    dict(
        confirmation_no="TESTE0035", guest_name_id="G0034",
        full_name="TITULAR, TESTE 34",
        arrival="15/10/26", departure="17/10/26",
        trunc_begin="15-OCT-26", trunc_end="17-OCT-26",
        room_no="403",
    ),
    dict(
        confirmation_no="TESTE0036", guest_name_id="G0034",  # mesmo hóspede
        full_name="CONVIDADO 01, TESTE 34",
        arrival="17/10/26", departure="19/10/26",  # gap zero
        trunc_begin="17-OCT-26", trunc_end="19-OCT-26",
        room_no="404",
    ),

    # 25c: mesmo GUEST_NAME_ID, reservas com GAP GRANDE (~2 meses) --
    # devem contar como 2 periodos distintos (limitação conhecida e
    # aceita, decision-log 2026-08-28).
    dict(
        confirmation_no="TESTE0037", guest_name_id="G0035",
        full_name="TITULAR, TESTE 35",
        arrival="05/07/26", departure="07/07/26",
        trunc_begin="05-JUL-26", trunc_end="07-JUL-26",
        room_no="405",
    ),
    dict(
        confirmation_no="TESTE0038", guest_name_id="G0035",  # mesmo hóspede
        full_name="CONVIDADO 01, TESTE 35",
        arrival="28/08/26", departure="30/08/26",
        trunc_begin="28-AUG-26", trunc_end="30-AUG-26",
        room_no="406",
    ),
]


# ---------------------------------------------------------------------
# Cenários 23 e 26 -- pares base (arquivo 1) / reimportação (arquivo 2).
# ---------------------------------------------------------------------

CENARIOS_REIMPORTACAO_BASE = [
    # 23 (base): quarto ainda nao atribuido -- sera preenchido na
    # reimportacao (arquivo 2).
    dict(
        confirmation_no="TESTE0039", guest_name_id="G0036",
        full_name="TESTE, HOSPEDE 36",
        arrival="12/10/26", departure="14/10/26",
        trunc_begin="12-OCT-26", trunc_end="14-OCT-26",
        room_no="",
    ),
    # 26 (base): titularidade original, sera trocada na reimportacao
    # (arquivo 2) -- correcao de titularidade feita pela recepcao no
    # ato do check-in (decision-log 2026-08-28).
    dict(
        confirmation_no="TESTE0040", guest_name_id="G0037",
        full_name="TITULAR, TESTE 37",
        arrival="13/10/26", departure="15/10/26",
        trunc_begin="13-OCT-26", trunc_end="15-OCT-26",
        room_no="410",
    ),
]

CENARIOS_REIMPORTACAO_V2 = [
    # 23: mesmo reservation_code de TESTE0039, ROOM_NO agora preenchido.
    dict(
        confirmation_no="TESTE0039", guest_name_id="G0036",
        full_name="TESTE, HOSPEDE 36",
        arrival="12/10/26", departure="14/10/26",
        trunc_begin="12-OCT-26", trunc_end="14-OCT-26",
        room_no="501",
    ),
    # 26: mesmo reservation_code de TESTE0040, GUEST_NAME_ID diferente
    # -- titularidade corrigida para quem efetivamente ocupou o quarto.
    dict(
        confirmation_no="TESTE0040", guest_name_id="G0038",  # mudou!
        full_name="CONVIDADO 01, TESTE 38",
        arrival="13/10/26", departure="15/10/26",
        trunc_begin="13-OCT-26", trunc_end="15-OCT-26",
        room_no="410",
    ),
]


def run() -> tuple[list[str], int]:
    """
    Gera os dois arquivos de fixture em tests/fixtures/:
    - res_detail_sintetico.xml: 40 reservas cobrindo os cenários
      combinados com a usuária (controle-base, share de quarto,
      status, fidelidade ALL, rate codes, comentários, keywords,
      traces, e as bases dos cenários de reimportação).
    - res_detail_sintetico_v2.xml: reimportação, com apenas as 2
      reservas que mudam (cenários 23 e 26).
    """
    todos_cenarios_arquivo1 = (
        CENARIOS_BLOCO_1 + CENARIOS_BLOCO_2 + CENARIOS_BLOCO_3
        + CENARIOS_REIMPORTACAO_BASE
    )
    reservas_arquivo1 = [
        montar_reserva(**params) for params in todos_cenarios_arquivo1
    ]

    # Cenário 1: múltiplos G_GROUP_BY1, tamanhos bem desiguais.
    # Calculado dinamicamente para não quebrar se a lista de cenários
    # mudar no futuro.
    total = len(reservas_arquivo1)
    tamanhos = [1, 3, total - 4]
    grupos = distribuir_em_grupos(reservas_arquivo1, tamanhos)
    raiz1 = montar_xml_completo(grupos)
    ET.indent(raiz1, space="  ")
    arvore1 = ET.ElementTree(raiz1)
    caminho1 = os.path.join("tests", "fixtures", "res_detail_sintetico.xml")
    os.makedirs(os.path.dirname(caminho1), exist_ok=True)
    arvore1.write(caminho1, encoding="utf-8", xml_declaration=True)

    # Arquivo 2: reimportação -- só as reservas que mudam.
    reservas_arquivo2 = [
        montar_reserva(**params) for params in CENARIOS_REIMPORTACAO_V2
    ]
    grupos2 = distribuir_em_grupos(reservas_arquivo2, [len(reservas_arquivo2)])
    raiz2 = montar_xml_completo(grupos2)
    ET.indent(raiz2, space="  ")
    arvore2 = ET.ElementTree(raiz2)
    caminho2 = os.path.join(
        "tests", "fixtures", "res_detail_sintetico_v2.xml"
    )
    arvore2.write(caminho2, encoding="utf-8", xml_declaration=True)

    total_reservas = len(reservas_arquivo1) + len(reservas_arquivo2)
    return [caminho1, caminho2], total_reservas
