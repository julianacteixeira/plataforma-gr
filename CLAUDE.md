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

A lista completa e sempre atualizada dos models está em
`app/models/__init__.py` — consultar sempre esse arquivo, nunca presumir a
partir do exemplo acima nem de qualquer lista em documentação.

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

## Dados de hóspede — LGPD

Arquivos reais do Opera Cloud (relatórios RES_DETAIL) PODEM ser usados como
entrada para análise de estrutura e teste do parser — são dados operacionais
do próprio hotel, e não há versão anonimizada disponível de origem. O que não
pode é o dado PERMANECER em algum lugar.

Regras:
- Arquivo real NUNCA dentro da árvore do projeto, nem em pasta ignorada pelo
  Git. Manter fora de C:\Projetos\plataforma-gr.
- NUNCA commitar arquivo com dado real de hóspede.
- Ao analisar um arquivo real, extrair apenas estrutura de tags, formatos,
  contagens e valores de campos controlados (status, códigos de tarifa, tipos
  de comentário). Nomes, documentos, números de cartão, telefones e textos de
  comentário nunca são reproduzidos em documentação, commit ou conversa.
- Documentação registra estatística ("437 de 698 reservas"), nunca conteúdo.
- Exemplos e testes automatizados usam SEMPRE fixture sintético, com dados
  inventados e estrutura equivalente à real.
- O conteúdo do XML importado não é salvo em disco pela aplicação (decisão de
  2026-08-03): processado em memória e descartado; a rastreabilidade fica em
  ImportLog/ImportErrorRecord.

## Fonte da verdade

- **O arquivo em disco vence tudo**: memória, histórico de conversa e a
  documentação do próprio projeto. Documentação desatualizada NÃO é evidência
  contra o código.
- **Se qualquer premissa de uma instrução não bater com o arquivo real, PARE
  e relate ANTES de editar.** Não corrigir por conta própria, não completar
  texto que pareça faltar, não inferir intenção.
- **Saída truncada no terminal não é evidência de conteúdo errado.** O
  PowerShell corta linhas e exibe acentos incorretamente. Verificar sempre
  pelo arquivo em disco, com grep de padrões específicos.

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
5. **Nunca rodar `flask db upgrade` sem revisão prévia do arquivo de
   migração**, independentemente de o banco ter dados ou não. Ver a
   seção "Migrações e seed — regras obrigatórias".
6. **Nunca inventar regras de negócio** não documentadas em
   `docs/decisions/decision-log.md` ou `docs/technical/data-model.md`;
   se uma decisão de modelagem não estiver clara, perguntar em vez de
   assumir.
7. Ao concluir uma etapa, atualizar `docs/handoff/current-state.md` e
   `docs/handoff/next-steps.md`, e sugerir o commit final da sessão.

## Migrações e seed — regras obrigatórias

1. **Correção de dado semente vai no arquivo de seed, nunca em migração.**
   A migração roda ANTES do seed; num banco novo a tabela ainda está vazia e
   o UPDATE afeta zero linhas, sem gerar erro. Migração de dado só se
   justifica para dado operacional criado em runtime, que não tem seed
   correspondente. (Incidente registrado em decision-log.md, 2026-08-26.)

2. **Migração que altera dado deve verificar rowcount.** Um
   op.execute("UPDATE ...") que não encontra linha nenhuma NÃO gera erro.
   Usar op.get_bind() e conferir result.rowcount, levantando RuntimeError se
   o número for diferente do esperado.

3. **server_default é obrigatório ao adicionar coluna NOT NULL em tabela já
   existente.** O SQLite exige valor padrão mesmo quando a tabela está vazia,
   e o autogenerate do Alembic não inclui isso sozinho. Sempre revisar o
   arquivo gerado. (Casos: c70c5df8e7e3, c161f11a4dd5.)

4. **Toda constraint precisa de nome explícito.** O SQLite exige nome ao
   recriar tabela em modo batch; constraint sem nome faz a migração falhar.
   (Caso: 6ac2cc539f41.)

5. **downgrade() deve ser simétrico ao upgrade().** O autogenerate omite
   reversões de op.execute(); acrescentar manualmente.

6. **Nunca gerar e aplicar migração no mesmo passo.** Prompt A gera e mostra;
   Prompt B aplica, após aprovação explícita. O arquivo gerado deve ser lido
   antes de rodar.

7. **batch_alter_table no SQLite não é atômico.** Se uma migração falhar no
   meio, NÃO tentar de novo: rodar flask db current, inspecionar as tabelas, e
   relatar. Pode haver artefato órfão a remover manualmente.

## Ambiente local (Windows / PowerShell)

- Ativar o ambiente virtual: `.\venv\Scripts\Activate.ps1`
- Definir `FLASK_APP` a cada terminal novo: `$env:FLASK_APP = "app.py"`
- Instalar dependências a partir do `requirements.txt`:
  `pip install -r requirements.txt`

### Padrão de teste sem terminal interativo

`flask shell -c` NÃO existe nesta versão do Flask. Para consultar o banco ou
testar um model, usar:

```
python -c "from app import create_app; from app.models import [Model]; app = create_app(); ctx = app.app_context(); ctx.push(); [expressão]"
```

## Stack (versões confirmadas em uso)

- Python 3.14.5
- Flask 3.1.3
- Flask-SQLAlchemy 3.1.1 / SQLAlchemy 2.0.51
- Flask-Migrate 4.1.0 / Alembic 1.18.5
- python-dotenv (config via `.env`, nunca hardcoded)
- Flask-Login (autenticação implementada: login, logout, CSRF via
  Flask-WTF, rota protegida com @login_required)
- openpyxl (exportação XLSX — ainda não implementado)
- Banco: SQLite local, com plano de migração futura para PostgreSQL
- Front-end: HTML/CSS/JS com identidade editorial maximalista (ver
  `docs/design/design-system.md` quando definido)

## Integração futura com Opera Cloud

O sistema deve funcionar de forma completa sem essa integração. Quando for
implementada, o código deve ficar isolado em um módulo próprio, sem
dependências espalhadas pelo restante do sistema.
