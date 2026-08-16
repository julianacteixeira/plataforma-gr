\# Próximos Passos — Plataforma de Guest Relations



\## Category: revisão concluída

Revisão de Category concluída em 2026-08-06 (migração aea187b152c4). Ver
docs/decisions/decision-log.md, entrada "[2026-08-06] Fechamento
definitivo: Category — scope, grupo, prioridade, always_apply,
manual_only". Seed das 28 categorias também concluído em 2026-08-06, via
comando `flask seed-categories`.



\## Pendência em andamento: fluxo de UX/telas (não implementar ainda)

Sessão de 2026-08-06 abriu uma entrevista de UX em paralelo (fora deste
ambiente) para desenhar em texto o fluxo principal de telas: tela de
"Chegadas" (lista de reservas do dia/período com indicação de badge),
painel principal, tela de planejamento de vipagem (a pergunta sobre se
VipPlan precisa de um segundo campo de status, distinto de
delivery_status, para representar "planejamento sem conflito de
estoque, pronto para entrega" separado de "efetivamente entregue", já
foi RESOLVIDA em 2026-08-09 — implementada como
VipPlan.ready_for_delivery, commit 5862c5c; ver current-state.md),
relatório de requisição semanal em XLSX (filtrável por período, base
para o memorando de requisição à loja física do hotel — ver decisão de
06/08 sobre fim do estoque físico próprio), e tela de perfil do
hóspede. NÃO alterar models, telas ou rotas dessas telas ainda
pendentes até a usuária trazer o resultado consolidado dessa
entrevista.

Duas outras mudanças de schema já decididas nessa mesma entrevista
(decision-log.md, entrada de 2026-08-06, itens 5 e 6) também foram
implementadas em 2026-08-09: `Guest.preferences` (commit 50c97c9) e a
nova tabela `institutional_dates` (commit bf2005e) — ver
current-state.md. As telas em si (Chegadas, painel principal,
planejamento de vipagem, requisição semanal, perfil do hóspede)
continuam pendentes de desenho e implementação.

Atualização de 2026-08-12: o desenho de schema do memorando de
requisição citado acima foi fechado nesta data (decision-log.md,
entrada "[2026-08-12] Modelo de dados do Memorando (substitui
WeeklyRequisition)") e já está implementado. Models `Memorando`
(app/models/memorando.py) e `MemorandoLine`
(app/models/memorando_line.py) criados, registrados em
app/models/__init__.py, e migrados com sucesso (migração c4572c5bb013,
"Cria tabelas de memorando e adiciona preparation_sector", aplicada em
2026-08-12) — ver current-state.md. Na mesma migração, ItemType também
ganhou o campo `preparation_sector` (nullable=True, sem default — itens
já cadastrados ficam vazios até revisão manual, item a item).

O que ainda NÃO existe, apesar do schema estar pronto: nenhuma rota,
nenhum formulário, nenhuma lógica de geração de memorando, nenhum
cálculo de agregação de linhas por setor + data de entrega, e nenhuma
lógica de versionamento (gerar v2 a partir de v1, preencher
previous_version_id, travar edição depois de exported_at). Só as
tabelas existem — essa frente continua fora de "Próxima etapa a
executar" abaixo até a usuária decidir priorizá-la.



## Importação Opera Cloud: planejamento CONCLUÍDO em 2026-08-12

Mapeamento completo de campos e regras de badge fechado (ver
decision-log.md, entrada "[2026-08-12] Mapeamento de campos e regras
da importação Opera Cloud"). Implementação em 3 frentes:

1. **Migração de schema — CONCLUÍDA em 2026-08-16** (migração
   34c2442a159b, ver current-state.md):
   - `Reservation.dept_traces` (Text, nullable)
   - Nova tabela `ReservationNote` (substitui `Reservation.notes`)
   - `Category.opera_rate_code` (String, nullable, unique)
   - Correção de dado: `scope` das 3 categorias ALL Signature, de
     "guest" para "stay"
   - Correção de dado: `Pedido de Desculpas.manual_only = True`

2. **Seed de `CategoryKeyword`** — PRÓXIMA ETAPA: lista completa
   registrada no decision-log — ~90 entradas ao todo, incluindo
   combinações "E" (`termo1+termo2`).

3. **Módulo de importação** em `app/integrations/opera_cloud/`: parser
   do XML RES_DETAIL e lógica de upsert de Guest/Reservation/
   GuestBadge/StayBadge/ReservationNote, com entradas em AuditLog.
   Depende da Frente 2 (seed de CategoryKeyword) estar concluída.

Regra do projeto: nunca gerar e aplicar migração no mesmo passo —
Prompt A (gera e mostra) sempre antes de Prompt B (aplica), com
aprovação explícita da usuária entre os dois.



\## Já concluído nesta frente

- Rotas de login e logout implementadas em app/auth/routes.py
  (blueprint auth), usando login_user()/logout_user() do Flask-Login.
  LoginForm (Flask-WTF) valida e-mail e senha, com proteção CSRF via
  CSRFProtect registrado globalmente. Rota de exemplo /painel protegida
  com @login_required. Testado manualmente em 2026-08-02: login
  correto, logout, bloqueio de /painel sem sessão, e rejeição de senha
  incorreta com mensagem de erro.
- Configuração do Flask-Login concluída: LoginManager registrado em
  app/extensions.py e app/__init__.py, model User herdando de
  UserMixin, métodos set_password/check_password com hashing via
  werkzeug.security, e função load_user (user_loader) implementada.
  Testado manualmente pelo flask shell em 2026-08-02: senha correta
  retorna True, senha errada retorna False.
- Listeners de imutabilidade do AuditLog (before_update e before_delete)
  testados manualmente com sucesso via flask shell em 2026-08-02: as duas
  tentativas (alterar e apagar uma entrada existente) levantaram
  RuntimeError como esperado, e após rollback() o registro original
  permaneceu intacto no banco. Confirma que a imutabilidade decidida em
  2026-07-30 está de fato em vigor.
- Desenho de banco do MVP completo: os 6 models implementados (User,
  Guest, Reservation, VipPlan, VipItem, AuditLog), com migrações
  aplicadas.
- As 6 tabelas do MVP confirmadas no banco local: users, guests,
  reservations, vip_plans, vip_items, audit_logs.
- Todas as decisões de campos registradas no decision-log.md — uma
  entrada por model.
- Campos em aberto de Reservation (source, room_number, reservation_code)
  decididos e registrados no decision-log.md em 2026-07-30.
- Campos em aberto de VipPlan (obrigatoriedade, não-unicidade de
  reservation_id + planned_date, status/delivery_status como texto livre
  sem default) decididos e registrados no decision-log.md em 2026-07-30.
- Campos em aberto de VipItem (obrigatoriedade, cost opcional com tipo
  Numeric(10, 2), availability_status como texto livre, substituição por
  edição do registro existente com rastro no AuditLog) decididos e
  registrados no decision-log.md em 2026-07-30.
- Campos e regras do AuditLog (todos os campos obrigatórios, entity_id sem
  FK por ser polimórfico, details como Text, action como texto livre,
  Reservation no escopo de auditoria, imutabilidade via listeners com as
  duas limitações conhecidas) decididos e registrados no decision-log.md
  em 2026-07-30.



\## Pontos de atenção a resolver antes de fechar o MVP

Ver detalhes em docs/handoff/current-state.md:

- Padronizar `nullable=False` em created_at/updated_at nos models User,
  Guest e Reservation, para ficarem consistentes com VipPlan e VipItem.
- Definir o comportamento de delivered_at/delivered_by_id ao reverter uma
  entrega, quando a funcionalidade de marcar/desmarcar entrega for
  implementada.
- Definir a regra de cascata ao apagar um VipPlan (o que acontece com os
  VipItems ligados a ele). Nenhum ondelete foi definido nas FKs.



\## Lições técnicas (não bloqueantes, para não repetir erro)

- Migrações que usam `batch_alter_table` no SQLite (necessário para alterar
  ou remover coluna) não são totalmente atômicas: o SQLite recria a tabela
  por trás dos panos, e comandos anteriores da mesma migração podem já ter
  sido aplicados mesmo que um comando posterior falhe. Se uma migração
  falhar no meio, sempre rodar `flask db current` e conferir as tabelas
  via `inspect(db.engine).get_table_names()` antes de tentar aplicar de
  novo — pode ser necessário apagar manualmente um artefato órfão (tabela
  criada pela tentativa anterior) antes de reaplicar. Caso registrado em
  2026-08-03, migração 6ac2cc539f41 (guest_badges).



\## Etapas seguintes previstas (nesta ordem)

. Estrutura de pastas do projeto + Git/GitHub privado.

. Ambiente Python local (instalação, ambiente virtual, Flask "hello world"

&#x20;  mínimo, sem lógica de negócio).

. Modelagem do banco de dados (hóspedes, reservas, categorias VIP,

&#x20;  planejamentos de vipagem, itens, usuários, log de auditoria).

1\. Configuração de migrações (Flask-Migrate).

2\. Autenticação de usuários (Flask-Login).

3\. Importação manual de reservas + consulta de reservas/hóspedes.

4\. Marcar VIP + categoria VIP.

5\. Planejamento de vipagem + itens (custo, responsável, status).

6\. Histórico e auditoria de alterações.

7\. Exportação de relatório em XLSX.

8\. Aplicação da identidade visual editorial.

9\. Pós-MVP (estoque, prevenção de duplicidade, relatórios avançados).

10\. Integração futura isolada com Opera Cloud.



\## Regras a lembrar em toda nova sessão

\- Trabalhar uma etapa pequena por vez.

\- Explicar o plano antes de codificar.

* Considerar sempre o que é melhor para a rotina de Guest Relations de resort

\- Listar arquivos a criar/alterar antes de qualquer mudança.

\- Nunca usar dados reais de hóspedes.

\- Recomendar commit de segurança antes de alterações relevantes.

\- Não mudar stack, arquitetura, identidade visual ou escopo sem aprovação explícita.

## Pendência técnica (não bloqueante)

O PowerShell 5.1 (Windows PowerShell) exibe acentos e caracteres especiais

incorretamente ao usar Get-Content/notepad em arquivos .md via terminal

(mojibake). Os arquivos em si estão corretos (confirmado no GitHub). Causa

provável: limitação de code page do PowerShell 5.1. Solução futura:

migrar para PowerShell 7 (pwsh) como terminal padrão, ou sempre conferir

conteúdo visualmente pelo Notepad/GitHub em vez do console.

