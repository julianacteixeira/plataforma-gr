import itertools

from app.extensions import db
from app.models import Category, CategoryKeyword


def _keywords_gerentes_accor():
    cargos = ["gerente", "gg", "gm"]
    marcas = [
        "accor", "fairmont", "sofitel", "mgallery", "25hours",
        "mama shelter", "swissôtel", "pullman", "mercure", "mantis",
        "novotel", "tribe", "mantra", "adagio", "ibis", "jo&joe",
        "hotelf1", "jequitimar",
    ]
    return [f"{cargo}+{marca}" for cargo, marca in itertools.product(cargos, marcas)]


def _keywords_convidados_gerencia():
    fixas = ["daniel betiol", "natália tamassia", "milena aguiar"]
    nomes_curtos = ["daniel", "natália", "milena"]
    contextos = ["pedido", "vip", "convidado", "convidada", "amigo", "amiga"]
    combinacoes = [
        f"{nome}+{contexto}"
        for nome, contexto in itertools.product(nomes_curtos, contextos)
    ]
    return fixas + combinacoes


CATEGORY_KEYWORDS = {
    "Colaboradores Accor": ["colaborador accor"],
    "Diretores Accor": ["diretoria accor"],
    "Gerentes Accor": _keywords_gerentes_accor(),
    "Investidor": ["investidor", "cotista", "senpar", "hotelinvest"],
    "Influencer": [
        "influencer", "influenciador", "influenciadora", "creator",
        "content creator",
    ],
    "C-Suite": [
        "ceo", "chief executive officer", "presidente", "president",
        "chairman", "chairwoman", "chairperson", "diretor", "director",
        "vp", "evp", "svp", "country manager", "board member",
        "conselheiro", "conselheira", "managing partner",
    ],
    "Pax Querido": ["pax+querido", "pax+querida", "pax+amor"],
    "Aniversário": ["aniversário", "niver"],
    "Casamento": ["casamento"],
    "Lua de Mel/Romântico": ["lua de mel", "romântico"],
    "Voucher Novos Colaboradores": ["voucher novos colaboradores"],
    "Atenção Especial": ["vip", "mimo"],
    "Comemorações": ["comemoração", "celebração", "formatura", "aposentadoria"],
    "Vip Eventos": [
        "vip eventos", "evento vip", "cliente de eventos",
        "cliente importante", "cliente trouxe o evento",
        "responsável pelo evento",
    ],
    "Data de Fechamento": ["fechamento"],
    "Convidados Gerência": _keywords_convidados_gerencia(),
    "Organizador de Grupo": [
        "organizador do grupo", "líder do grupo", "responsável pelo grupo",
    ],
    "Pacote Contratado": [
        "pacote contratado", "kit festa", "festa exclusiva",
        "festa na varanda", "presente gentileza", "presente lembrança",
        "presente presença", "pacote romântico", "bolo+kg",
        "pacote+encanto", "pacote+memorável", "pacote+deslumbrante",
    ],
}


def run():
    """Popula CategoryKeyword a partir de CATEGORY_KEYWORDS.

    Idempotente: pula combinações category_id + keyword já existentes,
    então pode ser rodado quantas vezes for necessário. Categorias não
    encontradas pelo nome exato são avisadas e puladas, sem interromper
    o script.
    """
    criadas = 0
    puladas = 0
    for category_name, keywords in CATEGORY_KEYWORDS.items():
        categoria = Category.query.filter_by(name=category_name).first()
        if categoria is None:
            print(f"AVISO: categoria '{category_name}' não encontrada — pulando.")
            continue
        for keyword in keywords:
            keyword = keyword.lower()
            existente = CategoryKeyword.query.filter_by(
                category_id=categoria.id, keyword=keyword
            ).first()
            if existente is not None:
                puladas += 1
                continue
            db.session.add(
                CategoryKeyword(category_id=categoria.id, keyword=keyword)
            )
            criadas += 1
    db.session.commit()
    return criadas, puladas
