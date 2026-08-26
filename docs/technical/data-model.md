# Modelo de Dados — Plataforma de Guest Relations



Status: Aprovado para implementação inicial (MVP). Campos de status

controlado (enums) ficam propositalmente abertos nesta fase e serão

fechados durante a implementação, quando for possível visualizar as telas.



## Convenções gerais

- Toda tabela tem `id` (inteiro, chave primária, autoincremento).

- Campos de data/hora usam timestamp com fuso horário.

- Nenhum registro de VipPlan ou VipItem é apagado fisicamente sem

&#x20; justificativa registrada em AuditLog (rastreabilidade).

- Nomes de tabelas e campos em inglês (código); labels na interface em

&#x20; português.



---



## User (usuário do sistema)

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| name | string | |
| email | string | único, usado para login |
| password_hash | string | nunca texto puro |
| role | string | valores em aberto (ex: atendente, gerente) — não usado para restrição no MVP |
| active | boolean | permite desativar login sem apagar histórico |
| created_at | timestamp | |



## Guest (hóspede)

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| full_name | string | |
| document | string | dado sensível (LGPD) — nunca usar dado real em exemplos/testes |
| email | string | opcional |
| phone | string | opcional |
| opera_guest_id | string | opcional, único quando presente — identificador do perfil do hóspede no Opera Cloud (GUEST_NAME_ID) |
| vip | boolean | true quando o hóspede tem pelo menos um GuestBadge ativo (ver tabela GuestBadge) |
| all_member | boolean | participa do programa de fidelidade ALL |
| all_card_number | string | opcional, preenchido se all_member=true |
| pmid | string | opcional, PMID do hóspede no ALL |
| created_at | timestamp | |
| updated_at | timestamp | |



## GuestBadge (selo do hóspede)

Substitui o antigo campo Guest.vip_category (ver decisão de 2026-08-02
em decision-log.md). Um hóspede pode ter vários badges independentes,
cada um com sua própria origem e status.

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| guest_id | integer | FK -> Guest |
| label | string | ex: "Gold", "Habitué", "Aniversário", "Colaborador Accor" |
| source | string | "all_tier", "keyword_suggestion", "stay_count" ou "manual" |
| status | string | "active", "suggested" ou "rejected" |
| created_by_id | integer | FK -> User, opcional — nulo quando source é automático |
| created_at | timestamp | |
| updated_at | timestamp | |



## CategoryKeyword (palavra-chave de categoria)
Usada pela importação Opera Cloud para sugerir badges automaticamente
(GuestBadge ou StayBadge, roteado dinamicamente via Category.scope — ver
decisão de 2026-08-12 em decision-log.md). Busca por substring, case- e
acento-insensível. Suporta combinação "E" no formato `termo1+termo2`
(ambos precisam aparecer no comentário, em qualquer ordem, para a regra
bater).

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| category_id | integer | FK -> Category |
| keyword | string(100) | termo único ou combinação `termo1+termo2` |
| active | boolean | default True — permite desativar uma keyword sem apagar |
| created_by_id | integer | FK -> User, opcional — nulo quando a keyword vem de seed/carga automática |
| created_at | timestamp | |

Sem unicidade de `(category_id, keyword)` no banco — checagem de
duplicidade fica a cargo do código que popula a tabela (seed ou tela de
cadastro futura).



## Reservation (reserva)

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| guest_id | integer | FK -> Guest |
| check_in | date | |
| check_out | date | |
| room_number | string | quarto "padrão" da reserva |
| reservation_code | string | único — chave usada para evitar importação duplicada |
| source | string | valores em aberto (ex: manual, opera_cloud) |
| notes | text | opcional — observações vindas do Opera Cloud (RES_COMMENT), cada uma em um parágrafo, na ordem em que aparecem no relatório |
| created_at | timestamp | |



## VipPlan (Planejamento de Vipagem)

Representa um planejamento em um dia específico dentro de uma reserva.

Uma reserva pode ter vários VipPlans (ex: chegada, aniversário, saída).



| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| reservation_id | integer | FK -> Reservation |
| planned_date | date | dia ao qual este planejamento se refere |
| room_number_override | string | opcional — só preenchido se o quarto daquele dia for diferente do da reserva |
| status | string | valores em aberto (ex: planejado, em preparação, concluído, cancelado) |
| delivery_status | string | valores em aberto (ex: pendente, entregue) — aplicado ao conjunto inteiro |
| delivered_at | timestamp | opcional, preenchido quando delivery_status = entregue |
| delivered_by_id | integer | FK -> User, opcional, quem confirmou a entrega |
| created_by_id | integer | FK -> User |
| created_at | timestamp | |
| updated_at | timestamp | |



## VipItem (Item de Vipagem)

Um item individual dentro de um VipPlan. Pode ser editado (descrição,

custo, disponibilidade) independentemente dos outros itens do mesmo

planejamento; a confirmação de entrega, porém, é feita no nível do

VipPlan (conjunto), não item por item.



| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| vip_plan_id | integer | FK -> VipPlan |
| description | string | editável a qualquer momento |
| cost | decimal | editável a qualquer momento |
| responsible_id | integer | FK -> User |
| availability_status | string | valores em aberto (ex: planejado, indisponível, substituído) |
| created_at | timestamp | |
| updated_at | timestamp | |



## ItemType (cadastro de tipo de item)

Cadastro leve e reaproveitável de item usado em vipagens (ver decisão de
2026-08-03 em decision-log.md, "Desenho revisado de schema: Category,
ItemType, StayBadge, GuestLink"). Um item nunca antes usado numa vipagem
deve ser cadastrado aqui antes de ser referenciado por um VipItem.

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| name | string | único |
| default_cost | decimal | Numeric(10, 2) |
| cost_category | string | valores identificados: "A&B", "Brindes", "Papelaria" — classificação interna de custo, não confundir com preparation_sector |
| assembly_instructions | text | "ficha técnica": como o item deve ser montado/posicionado (talher, guardanapo, taça etc.) |
| preparation_sector | string | opcional (nullable=True, sem default) — valores: Cozinha, Confeitaria, A&B, Recepção, Loja. Determina o setor de cada linha de Memorando. Itens já cadastrados ficam com este campo vazio até revisão manual, item a item (decisão de 2026-08-12) |
| created_at | timestamp | |
| updated_at | timestamp | |



## Memorando (documento de requisição por setor)

Substitui o nome provisório WeeklyRequisition (ver decisão de
2026-08-12 em decision-log.md). Representa o memorando de requisição de
itens de vipagem à loja e demais setores do hotel. Mantém histórico
completo de versões — nenhuma versão é apagada; editar depois de
exportado significa gerar uma nova versão.

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| tipo | string | "consolidado" (agrega itens de vários VipPlans por setor + data de entrega) ou "pacote" (sempre vinculado a exatamente um VipPlan) |
| vip_plan_id | integer | FK -> VipPlan; obrigatório apenas quando tipo = "pacote", nulo em "consolidado" |
| version_number | integer | começa em 1 |
| previous_version_id | integer | FK -> Memorando (mesma tabela); nulo na v1 |
| status_versao | string | indica se é a versão vigente da linhagem ou se foi substituída por uma versão mais nova |
| responsavel_interno_id | integer | FK -> User — quem assume a responsabilidade pelo conteúdo perante o setor executor; editável enquanto exported_at estiver vazio |
| generated_by_id | integer | FK -> User — metadado técnico de quem operou o sistema; nunca aparece no arquivo exportado, nunca editável |
| generated_at | timestamp | metadado técnico, nunca editável |
| data_pedido | date | |
| observacao | text | texto livre |
| exported_at | timestamp | opcional; nulo até a primeira exportação. Uma vez preenchido, todo o conteúdo do memorando (inclusive responsavel_interno_id) vira imutável |
| forma_pagamento | string | exclusivo de tipo = "pacote" (nulo em "consolidado"); texto livre — valores identificados: "Pagamento antecipado", "Pagamento no checkout", "Cortesia", "Faturamento IBIOBI" |
| valor_total | decimal | exclusivo de tipo = "pacote" |
| pax_adultos | integer | exclusivo de tipo = "pacote" |
| pax_criancas_6_12 | integer | exclusivo de tipo = "pacote" |
| pax_criancas_ate_5 | integer | exclusivo de tipo = "pacote" |



## MemorandoLine (linha do memorando)

Uma linha vinculada a um VipItem representa sempre um único VipItem —
nunca uma linha agregada (decisão de 2026-08-12). O total por item
exibido no documento exportado é calculado na hora, agrupando linhas por
item_type_id + data_entrega; não é armazenado como valor próprio.

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| memorando_id | integer | FK -> Memorando |
| vip_item_id | integer | FK -> VipItem, opcional — nulo quando a linha é um item avulso/de sobra, sem vínculo a nenhum VipPlan |
| item_type_id | integer | FK -> ItemType, sempre preenchido, mesmo quando vip_item_id também está preenchido |
| quantidade | integer | |
| data_entrega | date | independente do planned_date do VipPlan de origem |
| horario | string | opcional |
| pax | integer | opcional, sempre digitado manualmente — nunca puxado automaticamente da Reservation |
| descricao_observacao | text | texto livre da linha, ex: "montar na Sala 4" |



## AuditLog (histórico de alterações)

Log manual explícito (Opção A): toda função que cria/altera VipPlan ou

VipItem também cria uma entrada aqui. Possível evoluir para captura

automática via eventos do SQLAlchemy no pós-MVP (Opção B).



| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| user_id | integer | FK -> User, quem fez a ação |
| entity_type | string | ex: VipPlan, VipItem, Reservation, GuestBadge |
| entity_id | integer | qual registro específico |
| action | string | valores em aberto (ex: criado, alterado, status alterado) |
| details | string | descrição legível da mudança |
| timestamp | timestamp | |



## ImportLog (registro de importação)

Apoio operacional para a importação Opera Cloud (Frente 3) — uma linha
por arquivo importado. Diferente do AuditLog (que registra decisões
humanas de vipagem e é imutável por design), ImportLog não é imutável:
é um registro técnico gerado pelo próprio sistema (decisão de
2026-08-24 em decision-log.md).

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| imported_by_id | integer | FK -> User |
| imported_at | timestamp | |
| filename | string | nome do arquivo enviado — o conteúdo do XML não é salvo em disco (decisão de 2026-08-03) |
| total_reservations | integer | |
| total_created | integer | |
| total_updated | integer | |
| total_cancelled | integer | |
| total_errors | integer | |

## ImportError (erro de importação)

Uma linha por reserva que falhou dentro de um import (decisão de
2026-08-24 em decision-log.md).

| Campo | Tipo | Observação |
|---|---|---|
| id | integer | PK |
| import_log_id | integer | FK -> ImportLog, indexado |
| confirmation_no | string | vem do XML; não é FK, pois a Reservation pode não ter chegado a ser criada |
| error_message | text | |
| created_at | timestamp | |



---



## Diagrama de relacionamento





Guest (1) ───< tem >─── Reservation (N)

Guest (1) ───< tem >─── GuestBadge (N)

Reservation (1) ───< pode gerar >─── VipPlan (N)

VipPlan (1) ───< contém >─── VipItem (N)

User (1) ───< cria >─── VipPlan (N)

User (1) ───< confirma entrega de >─── VipPlan (N)

User (1) ───< responsável por >─── VipItem (N)

User (1) ───< autor de >─── AuditLog (N)

VipItem (1) ───< referencia >─── ItemType (N)

VipPlan (1) ───< pode gerar (tipo pacote) >─── Memorando (N)

Memorando (1) ───< contém >─── MemorandoLine (N)

VipItem (1) ───< pode aparecer em >─── MemorandoLine (N)

ItemType (1) ───< referenciado por >─── MemorandoLine (N)

User (1) ───< responsável interno de >─── Memorando (N)

User (1) ───< gerou >─── Memorando (N)





## Decisões relacionadas

Ver `docs/decisions/decision-log.md`, entradas de 2026-07-23,
2026-08-02 (importação via Opera Cloud e sistema de badges de
GuestBadge), 2026-08-03 (ItemType, StayBadge, GuestLink e ajustes de
VipItem) e 2026-08-12 (Memorando e MemorandoLine, substituindo o nome
provisório WeeklyRequisition).



## Pendências para a fase de implementação

- Fechar os valores exatos de cada campo de status controlado (role,

&#x20; source, VipPlan.status, delivery_status,

&#x20; availability_status, AuditLog.action).

- Definir regra de validação para PMID/ALL card duplicados (pós-MVP).

- ItemType.preparation_sector fica nullable, sem valor default; itens
  já cadastrados ficam com o campo vazio até revisão manual, item a
  item (decisão de 2026-08-12) — nenhuma migração deve preencher esse
  campo automaticamente.

