\# Estado Atual do Projeto — Plataforma de Guest Relations



\*\*Última atualização:\*\* 2026-08-02



\## Fase atual

Desenho de banco do MVP concluído. Os seis models foram implementados um
a um, cada um com sua migração aplicada: User, Guest, Reservation,
VipPlan, VipItem e AuditLog. As 6 tabelas do MVP existem no banco local
(users, guests, reservations, vip_plans, vip_items, audit_logs) e todas as
decisões de campos estão registradas em docs/decisions/decision-log.md.

Com o banco desenhado, a próxima grande etapa é começar a camada de
autenticação (Flask-Login) ou as primeiras rotas/telas — a decidir na
próxima sessão.



\## O que já existe

\- Documentos de produto e decisões (docs/product/vision.md,

&#x20; docs/product/backlog.md, docs/decisions/decision-log.md).

\- Escopo definido: MVP, pós-MVP e integrações futuras (ver backlog.md).

\- Stack tecnológica definida (ver decision-log.md).

\- Identidade visual editorial definida (fundo off-white, Manrope, Instrument

&#x20; Serif, acentos coloridos, cards em camadas) — ainda não aplicada em

&#x20; nenhuma tela, pois nenhuma tela foi criada.

- Modelo de dados completo aprovado e documentado em
  docs/technical/data-model.md (6 tabelas: User, Guest, Reservation,
  VipPlan, VipItem, AuditLog).
- Modelo de dados completo aprovado e documentado (6 tabelas: User, Guest,
  Reservation, VipPlan, VipItem, AuditLog) — ver docs/technical/data-model.md.
- Ambiente Python local funcional (venv + Flask mínimo testado com sucesso).

- Aplicação Flask reestruturada em pacote (app/), com application factory
  (create_app()).
- SQLAlchemy e Flask-Migrate configurados e funcionando.
- Models implementados: User, Guest, Reservation, VipPlan, VipItem,
  AuditLog (todos os 6 do MVP).
- Primeira migração aplicada; banco SQLite local funcional
  (instance/plataforma_gr.db, fora do controle de versão).
- Model Reservation criado em app/models/reservation.py (FK guest_id ->
  guests.id, reservation_code único, source com default "manual"),
  registrado em app/models/__init__.py.
- Migração "Cria tabela de reservas" gerada e aplicada com sucesso; a
  tabela reservations existe no banco (confirmado via inspect: tabelas
  atuais = alembic_version, guests, reservations, users).
- Decisões sobre os campos em aberto de Reservation (source, room_number,
  reservation_code) registradas em docs/decisions/decision-log.md,
  entrada de 2026-07-30.
- Model VipPlan criado em app/models/vip_plan.py (FK reservation_id ->
  reservations.id, FKs delivered_by_id e created_by_id -> users.id, com
  relationships declarados via foreign_keys=[...] para desfazer a
  ambiguidade das duas FKs para a mesma tabela), registrado em
  app/models/__init__.py.
- Migração "Cria tabela de planos de vipagem" (0a9fd52b472e) gerada e
  aplicada com sucesso; a tabela vip_plans existe no banco (confirmado
  via inspect: tabelas atuais = alembic_version, guests, reservations,
  users, vip_plans).
- Decisões sobre os campos em aberto de VipPlan (obrigatoriedade dos
  campos, ausência de unicidade entre reservation_id e planned_date, e
  status/delivery_status como texto livre sem default) registradas em
  docs/decisions/decision-log.md, entrada de 2026-07-30.
- Model VipItem criado em app/models/vip_item.py (FK vip_plan_id ->
  vip_plans.id, FK responsible_id -> users.id, relationships simples sem
  foreign_keys=[...] porque cada FK aponta para uma tabela diferente;
  nenhum campo de entrega, nenhuma regra de ondelete), registrado em
  app/models/__init__.py.
- Migração "Cria tabela de itens de vipagem" (e12448617514) gerada e
  aplicada com sucesso; a tabela vip_items existe no banco (confirmado
  via inspect: tabelas atuais = alembic_version, guests, reservations,
  users, vip_items, vip_plans).
- Decisões sobre os campos em aberto de VipItem registradas em
  docs/decisions/decision-log.md, entrada de 2026-07-30: obrigatoriedade
  dos campos, `cost` opcional e com tipo Numeric(10, 2) (nunca Float, para
  evitar erro de arredondamento em valor monetário), availability_status
  como texto livre, e substituição de item feita por edição do registro
  existente, com rastreabilidade via entrada manual no AuditLog.
- Model AuditLog criado em app/models/audit_log.py (FK user_id ->
  users.id; entity_id é inteiro comum, SEM foreign key e SEM
  relationship, por ser relacionamento polimórfico — entity_type diz a
  qual tabela entity_id se refere; details usa Text, sem limite),
  registrado em app/models/__init__.py.
- Dois listeners de evento do SQLAlchemy no final de audit_log.py
  (before_update e before_delete) que levantam RuntimeError, impedindo
  que entradas de log sejam alteradas ou apagadas através do código da
  aplicação. TESTADO MANUALMENTE COM SUCESSO em 2026-08-02, via flask
  shell: as duas tentativas (alterar e apagar uma entrada) levantaram
  RuntimeError como esperado, e o registro original permaneceu intacto
  após rollback().
- Migração "Cria tabela de audit log" (bd1651bb9ab7) gerada e aplicada
  com sucesso; a tabela audit_logs existe no banco (confirmado via
  inspect: tabelas atuais = alembic_version, audit_logs, guests,
  reservations, users, vip_items, vip_plans).
- Decisões sobre os campos e regras do AuditLog registradas em
  docs/decisions/decision-log.md, entrada de 2026-07-30: todos os campos
  obrigatórios, entity_id sem FK, details como Text, action como texto
  livre, Reservation incluída no escopo de auditoria, e imutabilidade das
  entradas aplicada via listeners — com as duas limitações conhecidas
  registradas (não protege contra acesso direto ao banco nem contra um
  flask db downgrade desta migração).
- Flask-Login instalado e integrado: LoginManager registrado em
  app/extensions.py e inicializado em app/__init__.py; o model User
  passou a herdar de UserMixin, com métodos set_password/check_password
  usando hashing via werkzeug.security, e a função load_user (via
  @login_manager.user_loader) implementada em app/models/user.py. Login
  testado manualmente pelo flask shell em 2026-08-02: senha correta
  retorna True, senha errada retorna False.
- Autenticação completa via Flask-Login e Flask-WTF: blueprint auth com
  rotas /auth/login e /auth/logout (app/auth/routes.py), LoginForm
  (app/auth/forms.py) com validação de e-mail e proteção CSRF via
  CSRFProtect registrado globalmente em app/__init__.py, e rota de
  exemplo /painel protegida por @login_required. Testado manualmente
  em 2026-08-02: login correto, logout, bloqueio de /painel sem
  sessão, e rejeição de senha incorreta com mensagem de erro.
- Etapa 1 da importação Opera Cloud concluída (2026-08-03): schema
  alinhado às decisões de 2026-08-02. Model Guest perdeu vip_category e
  ganhou opera_guest_id (único, opcional); Reservation ganhou notes
  (Text, opcional); model novo GuestBadge criado em
  app/models/guest_badge.py e registrado em app/models/__init__.py.
  Migração 6ac2cc539f41 gerada e aplicada com sucesso; tabela
  guest_badges existe no banco e os campos alterados de guests e
  reservations foram confirmados via inspect. Durante a aplicação, a
  primeira tentativa falhou por a constraint unique gerada pelo
  autogenerate não ter nome (SQLite exige nome de constraint ao
  recriar tabela em modo batch) — corrigido nomeando a constraint como
  uq_guests_opera_guest_id no arquivo de migração. A falha deixou a
  tabela guest_badges criada de forma órfã (SQLite roda DDL sem
  transação); ela foi apagada manualmente (estava vazia) antes de
  reaplicar a migração com sucesso.
- Revisão adicional de schema concluída (2026-08-03), decorrente da
  revisão de escopo combinada com a usuária (ver decision-log.md,
  entradas "Revisão de escopo: GuestBadge, campos de contato, ItemType e
  templates de sugestão" e "Desenho revisado de schema: Category,
  ItemType, StayBadge, GuestLink"). Migração 730b36ea5422 gerada,
  corrigida (mesma classe de problema de nome de constraint da migração
  anterior, desta vez em duas foreign keys sem nome, e um NOT NULL sem
  server_default em reservations.contact_status) e aplicada com sucesso.
  Verificado via flask db current (730b36ea5422, head) e via flask shell
  (inspect(db.engine).get_table_names()):
  - 5 tabelas novas: categories, stay_badges, item_types,
    category_item_templates, guest_links.
  - GuestBadge (app/models/guest_badge.py): campo label removido,
    substituído por category_id (FK -> categories.id).
  - VipItem (app/models/vip_item.py): novo campo item_type_id (FK ->
    item_types.id, obrigatório); description deixou de ser obrigatório
    (nullable=True), reservado para observação específica da instância
    do item, já que o nome do item agora vem de ItemType.
  - Reservation (app/models/reservation.py): novos campos confirmed_eta
    (string HH:MM, opcional) e contact_status (string, default
    "pendente").
- Fechamento definitivo da revisão de Category concluído (2026-08-06; ver
  decision-log.md, entrada "[2026-08-06] Fechamento definitivo: Category
  — scope, grupo, prioridade, always_apply, manual_only"). Migração
  aea187b152c4 gerada e aplicada com sucesso. Verificado via flask db
  current (aea187b152c4, head) e via flask shell
  (inspect(db.engine).get_table_names()):
  - 1 tabela nova: category_keywords.
  - Category (app/models/category.py): novos campos always_apply e
    manual_only (boolean, default False, nullable=False); campo
    suggestion_priority alterado para nullable=True.
- Comando `flask seed-categories` criado (app/seeds/categories.py,
  registrado em app/__init__.py) e executado com sucesso: 28 categorias
  populadas na tabela categories (6 always_apply, 2 manual_only, 20 no
  ranking normal de suggestion_priority 1-21). Confirmado via flask
  shell: Category.query.count() = 28.


\## O que NÃO existe ainda

\- Qualquer tela ou protótipo no Figma Make.
- Qualquer outra rota, view ou template da aplicação (além da
  autenticação, que já existe).
- Exportação em XLSX.
- Nenhum dado de teste no banco: as 6 tabelas existem, mas estão todas
  vazias.
- CategoryKeyword ainda está vazia (model e tabela existem, seed de
  palavras-chave pendente — depende do resultado da sessão de UX em
  andamento sobre o fluxo de reconhecimento de reservas VIP).



\## Pontos de atenção registrados para o futuro

Não bloqueiam o andamento atual, mas devem ser resolvidos antes de fechar
o MVP:

- Padronizar `nullable=False` em `created_at` e `updated_at` nos models
  Guest e Reservation, para ficarem consistentes com VipPlan, VipItem e
  User. Para User essa pendência já foi resolvida: `created_at` passou
  a `nullable=False` via migração a2a4cd39ed83, aplicada com sucesso em
  2026-08-02. Guest e Reservation continuam pendentes dessa
  padronização.
- Definir o comportamento de `delivered_at` e `delivered_by_id` ao
  reverter uma entrega (desmarcar), quando a funcionalidade de
  marcar/desmarcar entrega for implementada. Em aberto: limpar os dois
  campos ou preservar o registro anterior. A regra do projeto de nunca
  apagar informação sem rastro sugere preservar, mas a decisão ainda não
  foi tomada.
- Definir a regra de cascata ao apagar um VipPlan: o que acontece com os
  VipItems ligados a ele. Nenhum `ondelete` foi definido nas FKs, por
  decisão de 2026-07-30 — será resolvido quando a funcionalidade de
  cancelar/apagar um planejamento for desenhada. Atenção: o SQLite só
  aplica restrições de chave estrangeira se `PRAGMA foreign_keys`
  estiver ligado, e por padrão ele vem desligado; não concluir pelo
  teste local que "o banco deixou apagar".


\## Como retomar o trabalho

1\. Leia este arquivo e `docs/handoff/next-steps.md`.

2\. Leia `docs/decisions/decision-log.md` para não repetir decisões já

&#x20;  tomadas.

3\. Confirme com o usuário se algo mudou desde a última atualização deste

&#x20;  arquivo antes de prosseguir.

