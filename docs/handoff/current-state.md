# Estado Atual do Projeto — Plataforma de Guest Relations

**Última atualização:** 2026-08-28

## Fase atual

Backend em construção, sem nenhuma interface. O banco tem 19 tabelas
aplicadas e a autenticação funciona. A frente ativa é a importação do
relatório RES_DETAIL do Opera Cloud, dividida em 3 frentes: schema
(concluída), seed de palavras-chave (concluída) e módulo de importação
(em andamento — Frente 3, Fatia 0 concluída).

O bloqueio registrado em 2026-08-24 — faltavam os nomes de 4 tags do XML
— foi RESOLVIDO em 2026-08-26 com acesso a um arquivo RES_DETAIL real de
698 reservas. A Frente 3 está liberada para começar.

A Fatia 0 da Frente 3 (fixture sintético) foi concluída em 2026-08-28
(commits até b08e0e7): 40 reservas + arquivo de reimportação, cobrindo 28
cenários de negócio, incluindo o mapeamento de campos
title/RES_COMMENT/GTV_TRACE_ON confirmado contra um relatório real.
Próximo passo: Fatia 1 (parser puro do XML).

## O que já existe

### Documentação
- Produto e decisões: docs/product/vision.md, docs/product/backlog.md,
  docs/decisions/decision-log.md.
- Referência de campos do Opera Cloud confirmados contra um relatório
  real: docs/technical/opera-field-reference.md (comentários de reserva,
  título, traces internos).
- Modelo de dados completo em docs/technical/data-model.md: as 19
  tabelas documentadas, com diagrama de relacionamento organizado em 6
  blocos temáticos (commits 06d1e48, 2a4a423, f6b7698).
- CLAUDE.md com as regras de trabalho, incluindo as regras novas de
  migração/seed criadas em 2026-08-26 (commit 4144c1e).
- Identidade visual editorial definida (off-white, Manrope, Instrument
  Serif, acentos coloridos, cards em camadas) — ainda não aplicada em
  nenhuma tela, pois nenhuma tela existe.

### Aplicação
- Aplicação Flask em pacote (app/), com application factory
  (create_app()). SQLAlchemy e Flask-Migrate configurados.
- Autenticação completa: blueprint auth com /auth/login e /auth/logout,
  LoginForm (Flask-WTF), CSRFProtect global, rota de exemplo /painel
  protegida com @login_required. Testada manualmente em 2026-08-02.
- Imutabilidade do AuditLog via listeners before_update/before_delete,
  testada manualmente em 2026-08-02 (as duas tentativas levantaram
  RuntimeError; o registro permaneceu intacto após rollback).
  Limitações conhecidas registradas: não protege contra acesso direto ao
  banco nem contra flask db downgrade da migração.

### Banco de dados
Migração corrente: 8301e98c75e9 (head). 17 arquivos de migração em
migrations/versions.

20 tabelas no banco (19 do modelo + alembic_version):
alembic_version, audit_logs, categories, category_item_templates,
category_keywords, guest_badges, guest_links, guests, import_errors,
import_logs, institutional_dates, item_types, memorando_lines,
memorandos, reservation_notes, reservations, stay_badges, users,
vip_items, vip_plans.

### Dados semente no banco
O banco NÃO está vazio. Estado verificado em 2026-08-26:
- 29 categorias (6 always_apply, 3 manual_only, 4 com opera_rate_code
  preenchido; 17 scope="stay", 12 scope="guest").
- 140 CategoryKeyword, distribuídas em 18 categorias, via o comando
  idempotente `flask seed-category-keywords`.
- As 4 categorias com opera_rate_code: ACO (Colaboradores Accor,
  guest), ALSIG1 (ALL Signature Zen Day, stay), ALSIG2 (ALL Signature
  Fondue, stay), ALSIG3 (ALL Signature ALL Kids, stay).

### Importação Opera Cloud — Frente 1 (schema): CONCLUÍDA
Migração 34c2442a159b (2026-08-16): nova tabela reservation_notes;
Reservation ganhou dept_traces e perdeu notes; Category ganhou
opera_rate_code (unique nomeada).

Migração c161f11a4dd5 (2026-08-26, commit 87d9a32): 4 campos novos em
Reservation, derivados da análise do XML real —
- opera_status (String(10), nullable) — SHORT_RESV_STATUS cru
- is_shared (Boolean, NOT NULL, server_default=false) — IS_SHARED_YN
- adults (Integer, nullable) — ADULTS
- children (Integer, nullable) — CHILDREN
Correção manual necessária em is_shared: o autogenerate não inclui
server_default, e o SQLite exige valor padrão para adicionar coluna NOT
NULL em tabela existente. Mesma lição da migração c70c5df8e7e3.

Migração 6e00db0bda48 (commit 07f958d): tabelas import_logs e
import_errors. A classe chama-se ImportErrorRecord (não ImportError),
para não colidir com a exceção nativa do Python. São tabelas de apoio
operacional, não de auditoria: sem listeners de imutabilidade, fora do
escopo do AuditLog, podendo ser limpas no futuro.

### Importação Opera Cloud — Frente 2 (seed de keywords): CONCLUÍDA
app/seeds/category_keywords.py, comando `flask seed-category-keywords`,
idempotente. 140 keywords em 18 categorias.

### Importação Opera Cloud — Frente 3, Fatia 0 (fixture sintético): CONCLUÍDA
app/cli/test_fixtures.py, comando `flask generate-test-fixtures` (commits
8f21f96 e b08e0e7). Gera tests/fixtures/res_detail_sintetico.xml (40
reservas, 28 cenários de negócio combinados: status, share de quarto,
fidelidade ALL, rate codes, comentários/keywords, traces) e
tests/fixtures/res_detail_sintetico_v2.xml (reimportação, cenários 23 e
26 — quarto atribuído depois e correção de titularidade). Todos os dados
são inventados. Próxima etapa: Fatia 1 (parser puro do XML).

### Correção do incidente de camada errada (commit 9620dd2)
Descoberto em 2026-08-26 que duas correções de dado embutidas na
migração 34c2442a159b nunca surtiram efeito, e que opera_rate_code nunca
fora preenchido. Causa raiz: correção de dado semente aplicada em
migração, quando deveria estar no arquivo de seed. Corrigido em
app/seeds/categories.py; `flask seed-categories` atualizou o banco no
mesmo movimento (0 criadas / 29 atualizadas). Ver decision-log.md,
entrada "[2026-08-26] Incidente: correção de dado aplicada na camada
errada", que também registra as duas regras novas derivadas.

### Estrutura do XML RES_DETAIL confirmada (commits 48ea5e4, 4a9ac4f)
Análise de arquivo real de 698 reservas, sem manter nenhum dado de
hóspede. Confirmou a hierarquia de tags, as 4 tags que faltavam
(ARRIVAL, DEPARTURE, ROOM_NO, FULL_NAME), a armadilha do agrupamento por
data de chegada (múltiplos G_GROUP_BY1), a correção de
ReservationNote.order_by, e o modelo correto de share de quarto. Ver
decision-log.md, as duas entradas de 2026-08-26.

## O que NÃO existe ainda

- Qualquer tela, rota ou template além da autenticação.
- Qualquer protótipo no Figma Make.
- A pasta app/integrations/ — a Frente 3 (parser + upsert) não começou.
- Exportação em XLSX.
- Memorando: só o schema existe (models + migração c4572c5bb013). Nenhuma
  rota, formulário, lógica de geração, cálculo de agregação por setor +
  data de entrega, nem lógica de versionamento. As tabelas memorandos e
  memorando_lines estão vazias.
- Catálogo/Pacotes e Requisição Semanal: nem schema.
- Nenhum dado operacional no banco: guests, reservations, vip_plans e
  demais tabelas de operação estão vazias. Só as tabelas de dados semente
  (categories, category_keywords) estão populadas.

## Pontos de atenção registrados para o futuro

Não bloqueiam o andamento atual, mas devem ser resolvidos antes de
fechar o MVP:

- Padronizar nullable=False em created_at/updated_at nos models que
  ainda divergem do padrão de VipPlan/VipItem: Guest.updated_at
  (nullable=True) e Reservation.created_at (sem nullable=False,
  verificado em 2026-08-28). Reservation.updated_at já nasceu no
  padrão correto (migração 8301e98c75e9). User não possui coluna
  updated_at.
- Definir o comportamento de delivered_at/delivered_by_id ao reverter
  uma entrega. Em aberto: limpar os dois campos ou preservar o registro
  anterior.
- Definir a regra de cascata ao apagar um VipPlan. Nenhum ondelete foi
  definido nas FKs (decisão de 2026-07-30). Atenção: o SQLite só aplica
  restrições de chave estrangeira com PRAGMA foreign_keys ligado, e o
  padrão é desligado — não concluir pelo teste local que "o banco
  deixou apagar".
- Risco de entrega duplicada em quarto compartilhado: duas ou mais
  reservas no mesmo quarto geram dois ou mais planejamentos possíveis
  para a mesma data. Não se resolve no parser; resolve-se agrupando
  visualmente as reservas irmãs na interface. Pendência da fase de
  telas (decisão de 2026-08-26).
- Formatação corrompida (escapes `\#`, `\-`, `\*\*` e `&#x20;`) nos demais
  arquivos de docs/, herdada de uma conversão antiga. Já corrigida em
  data-model.md (commit f181475) e neste arquivo; falta em vision.md,
  backlog.md, next-steps.md, system-blueprint.md, design-system.md,
  approved-ui-notes.md, opera-integration-plan.md e na metade antiga do
  decision-log.md. Cosmético, mas prejudica a leitura no GitHub.
- backlog.md desatualizado: todos os itens de Fundação continuam
  marcados como pendentes, incluindo migrações e login, que estão
  concluídos.

## Como retomar o trabalho

1. Leia este arquivo e docs/handoff/next-steps.md.
2. Leia docs/decisions/decision-log.md para não repetir decisões já
   tomadas.
3. Rode `git log --oneline -15` e `flask db current` e confirme que
   batem com o que está descrito aqui. Arquivo em disco e banco são
   fonte da verdade — inclusive contra esta documentação.
4. Confirme com a usuária se algo mudou desde a última atualização.
