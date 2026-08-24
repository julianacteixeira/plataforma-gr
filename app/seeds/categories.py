from app.extensions import db
from app.models import Category

CATEGORIES = [
    # Sempre-prioritárias (always_apply=True) - somam itens entre si,
    # ignoram o ranking normal, nunca competem sozinhas.
    {"name": "ALL Signature Zen Day", "scope": "guest", "group_number": 1,
     "always_apply": True, "manual_only": False, "suggestion_priority": None},
    {"name": "ALL Signature Fondue", "scope": "guest", "group_number": 1,
     "always_apply": True, "manual_only": False, "suggestion_priority": None},
    {"name": "ALL Signature ALL Kids", "scope": "guest", "group_number": 1,
     "always_apply": True, "manual_only": False, "suggestion_priority": None},
    {"name": "Voucher Novos Colaboradores", "scope": "stay", "group_number": 7,
     "always_apply": True, "manual_only": False, "suggestion_priority": None},
    {"name": "Ações", "scope": "stay", "group_number": 8,
     "always_apply": True, "manual_only": False, "suggestion_priority": None},
    {"name": "Pacote Contratado", "scope": "stay", "group_number": 9,
     "always_apply": True, "manual_only": False, "suggestion_priority": None},

    # Manual only - nunca entram automaticamente, suggestion_priority
    # aqui serve só para posicionamento visual na tela.
    {"name": "Pax Querido", "scope": "guest", "group_number": 1,
     "always_apply": False, "manual_only": True, "suggestion_priority": 20},
    {"name": "IBIOBI", "scope": "stay", "group_number": 1,
     "always_apply": False, "manual_only": True, "suggestion_priority": 22},

    # Ranking normal - competem entre si quando nenhuma always_apply
    # está presente; só a de maior prioridade (menor número) vence.
    {"name": "Data de Fechamento", "scope": "stay", "group_number": 6,
     "always_apply": False, "manual_only": False, "suggestion_priority": 1},
    {"name": "Habitué/Habituée", "scope": "guest", "group_number": 8,
     "always_apply": False, "manual_only": False, "suggestion_priority": 2},
    {"name": "Pedido de Desculpas", "scope": "stay", "group_number": 6,
     "always_apply": False, "manual_only": False, "suggestion_priority": 3},
    {"name": "Aniversário", "scope": "stay", "group_number": 4,
     "always_apply": False, "manual_only": False, "suggestion_priority": 4},
    {"name": "Investidor", "scope": "guest", "group_number": 3,
     "always_apply": False, "manual_only": False, "suggestion_priority": 5},
    {"name": "Diretores Accor", "scope": "guest", "group_number": 3,
     "always_apply": False, "manual_only": False, "suggestion_priority": 6},
    {"name": "Comemorações", "scope": "stay", "group_number": 4,
     "always_apply": False, "manual_only": False, "suggestion_priority": 7},
    {"name": "Gerentes Accor", "scope": "guest", "group_number": 2,
     "always_apply": False, "manual_only": False, "suggestion_priority": 8},
    {"name": "Convidados Gerência", "scope": "stay", "group_number": 3,
     "always_apply": False, "manual_only": False, "suggestion_priority": 9},
    {"name": "Vip Eventos", "scope": "stay", "group_number": 5,
     "always_apply": False, "manual_only": False, "suggestion_priority": 10},
    {"name": "ALL Diamond", "scope": "guest", "group_number": 3,
     "always_apply": False, "manual_only": False, "suggestion_priority": 11},
    {"name": "ALL Limitless", "scope": "guest", "group_number": 3,
     "always_apply": False, "manual_only": False, "suggestion_priority": 11},
    {"name": "Lua de Mel/Romântico", "scope": "stay", "group_number": 4,
     "always_apply": False, "manual_only": False, "suggestion_priority": 12},
    {"name": "ALL Platinum", "scope": "guest", "group_number": 2,
     "always_apply": False, "manual_only": False, "suggestion_priority": 13},
    {"name": "Atenção Especial", "scope": "stay", "group_number": 1,
     "always_apply": False, "manual_only": False, "suggestion_priority": 14},
    {"name": "Colaboradores Accor", "scope": "guest", "group_number": 1,
     "always_apply": False, "manual_only": False, "suggestion_priority": 15},
    {"name": "Influencer", "scope": "guest", "group_number": 3,
     "always_apply": False, "manual_only": False, "suggestion_priority": 16},
    {"name": "Casamento", "scope": "stay", "group_number": 4,
     "always_apply": False, "manual_only": False, "suggestion_priority": 17},
    {"name": "ALL Gold", "scope": "guest", "group_number": 1,
     "always_apply": False, "manual_only": False, "suggestion_priority": 18},
    {"name": "C-Suite", "scope": "guest", "group_number": 2,
     "always_apply": False, "manual_only": False, "suggestion_priority": 19},
    {"name": "Organizador de Grupo", "scope": "stay", "group_number": 1,
     "always_apply": False, "manual_only": False, "suggestion_priority": 21},
]


def run():
    """Insere ou atualiza as categorias definidas em CATEGORIES.

    Idempotente: identifica categorias existentes pelo campo `name` e
    atualiza os campos em vez de duplicar, então pode ser rodado
    quantas vezes for necessário.
    """
    criadas = 0
    atualizadas = 0
    for dados in CATEGORIES:
        categoria = Category.query.filter_by(name=dados["name"]).first()
        if categoria is None:
            categoria = Category(**dados)
            db.session.add(categoria)
            criadas += 1
        else:
            for campo, valor in dados.items():
                setattr(categoria, campo, valor)
            atualizadas += 1
    db.session.commit()
    return criadas, atualizadas
