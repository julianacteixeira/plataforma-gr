# Contexto do Projeto para Claude / Claude Code / Cowork

Este arquivo existe para que qualquer sessão de IA (Claude no chat, Claude
Code, Cowork) entenda rapidamente o projeto sem precisar reler todo o
histórico de conversas.

## Leitura obrigatória antes de qualquer alteração

1. `docs/handoff/current-state.md` — estado atual
2. `docs/handoff/next-steps.md` — próximo passo combinado
3. `docs/decisions/decision-log.md` — decisões já aprovadas (não reverter
   sem confirmar com o usuário)
4. `docs/technical/data-model.md` — desenho das tabelas do banco de dados

## Estrutura real do projeto (não presumir outra)

```
plataforma-gr/
├── app.py                  # ponto de entrada; importa create_app() de app/
├── config.py               # lê configurações do .env (nunca hardcode segredos)
├── requirements.txt
├── app/
│   ├── __init__.py         # contém create_app() (application factory)
│   ├── extensions.py       # instâncias únicas: db (SQLAlchemy), migrate
│   └── models/
│       ├── __init__.py     # importa e reexporta todos os models
│       ├── user.py         # class User
│       └── guest.py        # class Guest
├── migrations/              # gerado pelo Flask-Migrate; não editar à mão
├── instance/ ou *.db na raiz # arquivo do banco SQLite (nunca versionar)
└── docs/                    # documentação do projeto (ver seção acima)
```

**Padrão obrigatório para novos models:** um arquivo por tabela dentro de
`app/models/` (ex: `app/models/reservation.py`), sempre importando
`db` de `app.extensions`, e sempre registrado em `app/models/__init__.py`.
Nunca criar um `models.py` solto na raiz — já aconteceu uma vez e gerou um
arquivo órfão e duplicado.

## Regras fixas deste projeto

- Nunca usar dados reais de hóspedes em código, testes ou exemplos.
- Nunca commitar o arquivo `.env` (ver `.gitignore`).
- Preferir poucas alterações por vez; não editar dezenas de arquivos de uma
  vez sem aprovação explícita do usuário.
- Recomendar um commit de segurança antes de alterações estruturais.
- Não alterar stack, arquitetura ou identidade visual sem justificar e
  obter aprovação.
- Confiabilidade dos dados de vipagem é a prioridade máxima do projeto:
  cada item registrado separadamente, status de plano e de item
  independentes, autor e data/hora de cada alteração, nunca apagar
  informação sem rastro.
- O usuário é iniciante em desenvolvimento. Qualquer termo técnico novo
  deve ser explicado (o que é, para que serve, como se aplica aqui) antes
  de ser usado sem explicação nas respostas seguintes.

## Regras adicionais para ferramentas agênticas (Claude Code / Cowork)

Estas ferramentas executam comandos e editam arquivos diretamente, sem o
usuário colar código manualmente — por isso exigem travas mais explícitas
do que uma conversa no chat:

1. **Análise antes de edição.** Ao receber uma tarefa nova, primeiro
   descrever o plano (quais arquivos serão criados/alterados e por quê) e
   aguardar confirmação do usuário antes de escrever qualquer arquivo.
2. **Um arquivo por vez**, salvo aprovação explícita para um grupo maior.
3. **Sempre sugerir um commit de segurança** (`git add . && git commit`)
   antes de iniciar qualquer alteração estrutural, e nunca fazer commit ou
   push sem o usuário pedir.
4. **Depois de editar, mostrar o `git diff`** do que foi alterado antes de
   considerar a tarefa concluída.
5. **Nunca rodar `flask db upgrade` em um banco que já tem dados** sem
   antes confirmar com o usuário — migrações podem apagar colunas/tabelas.
6. **Nunca inventar regras de negócio** não documentadas em
   `docs/decisions/decision-log.md` ou `docs/technical/data-model.md`;
   se uma decisão de modelagem não estiver clara, perguntar em vez de
   assumir.
7. Ao concluir uma etapa, atualizar `docs/handoff/current-state.md` e
   `docs/handoff/next-steps.md`, e sugerir o commit final da sessão.

## Ambiente local (Windows / PowerShell)

- Ativar o ambiente virtual: `.\venv\Scripts\Activate.ps1`
- Definir `FLASK_APP` a cada terminal novo: `$env:FLASK_APP = "app.py"`
- Instalar dependências a partir do `requirements.txt`:
  `pip install -r requirements.txt`

## Stack (versões confirmadas em uso)

- Python 3.14.5
- Flask 3.1.3
- Flask-SQLAlchemy 3.1.1 / SQLAlchemy 2.0.51
- Flask-Migrate 4.1.0 / Alembic 1.18.5
- python-dotenv (config via `.env`, nunca hardcoded)
- Flask-Login (autenticação — ainda não implementado)
- openpyxl (exportação XLSX — ainda não implementado)
- Banco: SQLite local, com plano de migração futura para PostgreSQL
- Front-end: HTML/CSS/JS com identidade editorial maximalista (ver
  `docs/design/design-system.md` quando definido)

## Integração futura com Opera Cloud

O sistema deve funcionar de forma completa sem essa integração. Quando for
implementada, o código deve ficar isolado em um módulo próprio, sem
dependências espalhadas pelo restante do sistema.
