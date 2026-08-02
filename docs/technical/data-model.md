\# Modelo de Dados — Plataforma de Guest Relations



Status: Aprovado para implementação inicial (MVP). Campos de status

controlado (enums) ficam propositalmente abertos nesta fase e serão

fechados durante a implementação, quando for possível visualizar as telas.



\## Convenções gerais

\- Toda tabela tem `id` (inteiro, chave primária, autoincremento).

\- Campos de data/hora usam timestamp com fuso horário.

\- Nenhum registro de VipPlan ou VipItem é apagado fisicamente sem

&#x20; justificativa registrada em AuditLog (rastreabilidade).

\- Nomes de tabelas e campos em inglês (código); labels na interface em

&#x20; português.



\---



\## User (usuário do sistema)

| Campo | Tipo | Observação |

|---|---|---|

| id | integer | PK |

| name | string | |

| email | string | único, usado para login |

| password\_hash | string | nunca texto puro |

| role | string | valores em aberto (ex: atendente, gerente) — não usado para restrição no MVP |

| active | boolean | permite desativar login sem apagar histórico |

| created\_at | timestamp | |



\## Guest (hóspede)

| Campo | Tipo | Observação |

|---|---|---|

| id | integer | PK |

| full\_name | string | |

| document | string | dado sensível (LGPD) — nunca usar dado real em exemplos/testes |

| email | string | opcional |

| phone | string | opcional |

| opera\_guest\_id | string | opcional, único quando presente — identificador do perfil do hóspede no Opera Cloud (GUEST\_NAME\_ID) |

| vip | boolean | true quando o hóspede tem pelo menos um GuestBadge ativo (ver tabela GuestBadge) |

| all\_member | boolean | participa do programa de fidelidade ALL |

| all\_card\_number | string | opcional, preenchido se all\_member=true |

| pmid | string | opcional, PMID do hóspede no ALL |

| created\_at | timestamp | |

| updated\_at | timestamp | |



\## GuestBadge (selo do hóspede)

Substitui o antigo campo Guest.vip\_category (ver decisão de 2026-08-02
em decision-log.md). Um hóspede pode ter vários badges independentes,
cada um com sua própria origem e status.

| Campo | Tipo | Observação |

|---|---|---|

| id | integer | PK |

| guest\_id | integer | FK -> Guest |

| label | string | ex: "Gold", "Habitué", "Aniversário", "Colaborador Accor" |

| source | string | "all\_tier", "keyword\_suggestion", "stay\_count" ou "manual" |

| status | string | "active", "suggested" ou "rejected" |

| created\_by\_id | integer | FK -> User, opcional — nulo quando source é automático |

| created\_at | timestamp | |

| updated\_at | timestamp | |



\## Reservation (reserva)

| Campo | Tipo | Observação |

|---|---|---|

| id | integer | PK |

| guest\_id | integer | FK -> Guest |

| check\_in | date | |

| check\_out | date | |

| room\_number | string | quarto "padrão" da reserva |

| reservation\_code | string | único — chave usada para evitar importação duplicada |

| source | string | valores em aberto (ex: manual, opera\_cloud) |

| notes | text | opcional — observações vindas do Opera Cloud (RES\_COMMENT), cada uma em um parágrafo, na ordem em que aparecem no relatório |

| created\_at | timestamp | |



\## VipPlan (Planejamento de Vipagem)

Representa um planejamento em um dia específico dentro de uma reserva.

Uma reserva pode ter vários VipPlans (ex: chegada, aniversário, saída).



| Campo | Tipo | Observação |

|---|---|---|

| id | integer | PK |

| reservation\_id | integer | FK -> Reservation |

| planned\_date | date | dia ao qual este planejamento se refere |

| room\_number\_override | string | opcional — só preenchido se o quarto daquele dia for diferente do da reserva |

| status | string | valores em aberto (ex: planejado, em preparação, concluído, cancelado) |

| delivery\_status | string | valores em aberto (ex: pendente, entregue) — aplicado ao conjunto inteiro |

| delivered\_at | timestamp | opcional, preenchido quando delivery\_status = entregue |

| delivered\_by\_id | integer | FK -> User, opcional, quem confirmou a entrega |

| created\_by\_id | integer | FK -> User |

| created\_at | timestamp | |

| updated\_at | timestamp | |



\## VipItem (Item de Vipagem)

Um item individual dentro de um VipPlan. Pode ser editado (descrição,

custo, disponibilidade) independentemente dos outros itens do mesmo

planejamento; a confirmação de entrega, porém, é feita no nível do

VipPlan (conjunto), não item por item.



| Campo | Tipo | Observação |

|---|---|---|

| id | integer | PK |

| vip\_plan\_id | integer | FK -> VipPlan |

| description | string | editável a qualquer momento |

| cost | decimal | editável a qualquer momento |

| responsible\_id | integer | FK -> User |

| availability\_status | string | valores em aberto (ex: planejado, indisponível, substituído) |

| created\_at | timestamp | |

| updated\_at | timestamp | |



\## AuditLog (histórico de alterações)

Log manual explícito (Opção A): toda função que cria/altera VipPlan ou

VipItem também cria uma entrada aqui. Possível evoluir para captura

automática via eventos do SQLAlchemy no pós-MVP (Opção B).



| Campo | Tipo | Observação |

|---|---|---|

| id | integer | PK |

| user\_id | integer | FK -> User, quem fez a ação |

| entity\_type | string | ex: VipPlan, VipItem, Reservation, GuestBadge |

| entity\_id | integer | qual registro específico |

| action | string | valores em aberto (ex: criado, alterado, status alterado) |

| details | string | descrição legível da mudança |

| timestamp | timestamp | |



\---



\## Diagrama de relacionamento





Guest (1) ───< tem >─── Reservation (N)

Guest (1) ───< tem >─── GuestBadge (N)

Reservation (1) ───< pode gerar >─── VipPlan (N)

VipPlan (1) ───< contém >─── VipItem (N)

User (1) ───< cria >─── VipPlan (N)

User (1) ───< confirma entrega de >─── VipPlan (N)

User (1) ───< responsável por >─── VipItem (N)

User (1) ───< autor de >─── AuditLog (N)





\## Decisões relacionadas

Ver `docs/decisions/decision-log.md`, entradas de 2026-07-23 e
2026-08-02 (importação via Opera Cloud e sistema de badges de
GuestBadge).



\## Pendências para a fase de implementação

\- Fechar os valores exatos de cada campo de status controlado (role,

&#x20; source, VipPlan.status, delivery\_status,

&#x20; availability\_status, AuditLog.action).

\- Definir regra de validação para PMID/ALL card duplicados (pós-MVP).

