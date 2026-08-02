\# Log de Decisões — Plataforma de Guest Relations



Formato de cada entrada:

\- \*\*Data\*\*

\- \*\*Decisão\*\*

\- \*\*Contexto/Motivo\*\*

\- \*\*Alternativas consideradas\*\*

\- \*\*Status\*\* (Aprovado / Pendente / Revisado)



\---



\## 2026-07-13 — Stack tecnológica inicial

\*\*Decisão:\*\* Python + Flask + HTML/CSS/JS + banco relacional via SQLAlchemy +

Flask-Migrate + Flask-Login + openpyxl.

\*\*Contexto:\*\* Usuário definiu stack antes do início do projeto, priorizando

simplicidade para iniciante e ecossistema maduro em Python.

\*\*Status:\*\* Aprovado.



\## 2026-07-13 — Identidade visual obrigatória

\*\*Decisão:\*\* Estética editorial maximalista e autoral; fundo off-white (nunca

creme); fontes Manrope (interface) e Instrument Serif (títulos editoriais);

cards com camadas e molduras; acentos em rosa, azul, verde, aqua e amarelo;

poucos gráficos; sem dashboards genéricos.

\*\*Contexto:\*\* Requisito de produto vindo do usuário, prioridade máxima sobre

tendências genéricas de dashboard.

\*\*Status:\*\* Aprovado.



\## 2026-07-13 — Opera Cloud como integração futura e isolada

\*\*Decisão:\*\* O MVP não depende da API do Opera Cloud. Importação inicial é

manual (arquivo). O código de integração futura ficará isolado do restante

do sistema (módulo/camada separada).

\*\*Contexto:\*\* API do Opera Cloud não está disponível/definida ainda; o

sistema precisa funcionar de forma independente.

\*\*Status:\*\* Aprovado.



\## 2026-07-13 — Banco de dados: SQLite em desenvolvimento, preparado para PostgreSQL

\*\*Decisão:\*\* Usar SQLite (arquivo local) durante o desenvolvimento do MVP,

usando SQLAlchemy como camada de abstração, permitindo migração futura para

PostgreSQL sem reescrever a lógica de negócio.

\*\*Contexto:\*\* SQLite não exige instalação de servidor de banco, ideal para

ambiente local de iniciante; SQLAlchemy garante portabilidade futura.

\*\*Alternativas consideradas:\*\* PostgreSQL desde o início (mais próximo de

produção, porém exige mais configuração inicial).

\*\*Status:\*\* Aprovado.



\## 2026-07-13 — Login individual por usuário

\*\*Decisão:\*\* Cada atendente de GR terá seu próprio login (não um login

compartilhado da equipe).

\*\*Contexto:\*\* Requisito de auditoria (saber quem alterou o quê) depende

diretamente de identificação individual de usuário.

\*\*Status:\*\* Aprovado.



\## 2026-07-13 — Modelo de dados da vipagem: Planejamento → Itens

\*\*Decisão:\*\* Um "Planejamento de Vipagem" pertence a uma reserva/hóspede e

contém vários "Itens de Vipagem" (relação um-para-muitos), cada item com

status, custo e responsável próprios.

\*\*Contexto:\*\* Estrutura necessária para permitir status independente por

item e histórico granular.

\*\*Status:\*\* Aprovado.



\## 2026-07-13 — Idioma do código vs. idioma da interface

\*\*Decisão:\*\* Código (nomes de variáveis, funções, tabelas) em inglês;

interface visível ao usuário em português.

\*\*Contexto:\*\* Prática padrão de mercado, facilita manutenção e uso de

bibliotecas/documentação.

\*\*Status:\*\* Aprovado.



\## 2026-07-15 — Projeto movido para fora do OneDrive

\*\*Decisão:\*\* O projeto passa a residir em `C:\\Projetos\\plataforma-gr`, fora de

qualquer pasta sincronizada pelo OneDrive.

\*\*Contexto:\*\* A tentativa inicial de criar o projeto em

`OneDrive – ACCOR\\Desktop\\plataforma-gr` causou dois problemas: (1) o

caractere de travessão no nome da pasta OneDrive gerou erros recorrentes de

caminho no PowerShell; (2) pastas sincronizadas pelo OneDrive podem gerar

conflitos com o Git (arquivos "somente na nuvem", sincronização da pasta

`.git`). Nenhum dado foi perdido durante a correção; os 5 documentos da

Etapa 1 foram movidos com sucesso para o novo local.

\*\*Alternativas consideradas:\*\* manter o projeto dentro do OneDrive (opção A,

descartada pelo risco de conflito com Git).

\*\*Status:\*\* Aprovado.



\---


## 2026-07-23 — Modelo de dados do MVP aprovado
**Decisão:** Aprovado o modelo de dados com 6 tabelas: User, Guest,
Reservation, VipPlan, VipItem, AuditLog. Reserva pode ter múltiplos
VipPlans (um por dia/ocasião). VipItem editável individualmente
(descrição, custo, disponibilidade); confirmação de entrega ocorre no
nível do VipPlan (conjunto), não por item. Guest inclui campos opcionais
de programa ALL (all_member, all_card_number, pmid). VipPlan inclui
room_number_override para os casos raros de troca de quarto durante a
estadia. Ver docs/technical/data-model.md para detalhes completos.
**Contexto:** Planejamento conjunto na Etapa 4, revisando cenários reais
de operação de Guest Relations.
**Status:** Aprovado.

## 2026-07-23 — Auditoria: log manual explícito (Opção A)
**Decisão:** AuditLog será alimentado manualmente e explicitamente pelo
código (cada função que altera VipPlan/VipItem também grava uma entrada),
em vez de captura automática via eventos do banco.
**Contexto:** Mais didático e depurável para fase de aprendizado; possível
migrar para captura automática no pós-MVP.
**Status:** Aprovado.

## 2026-07-23 — Valores de status controlado ficam abertos por ora
**Decisão:** Os valores exatos de campos como role, vip_category, source,
VipPlan.status, delivery_status, availability_status e AuditLog.action
não foram fechados nesta etapa; serão definidos durante a implementação,
quando for possível visualizar as telas reais.
**Contexto:** Preferência da usuária por refinar esses valores com
contexto visual, evitando retrabalho por decisão prematura.
**Status:** Aprovado.

## [2026-07-30] Campos em aberto do model Reservation

**Contexto:** o data-model.md definia a tabela Reservation, mas deixava três
pontos em aberto: os valores aceitos para `source`, a obrigatoriedade de
`room_number`, e o formato de `reservation_code`.

**Decisão:**
- `source`: aceitar apenas o valor `"manual"` nesta fase do projeto. O valor
  `"opera_cloud"` será adicionado (via migração simples) somente quando a
  integração com o Opera Cloud for implementada.
- `room_number`: campo opcional (nullable). Reservas podem ser importadas
  antes de o quarto ser atribuído.
- `reservation_code`: mantido como texto livre (string, único, não vazio),
  sem validação de formato ou tamanho fixo. Sistemas diferentes (importação
  manual hoje, Opera Cloud no futuro) podem gerar códigos em formatos
  distintos.

**Alternativas consideradas:**
- Incluir `"opera_cloud"` como valor válido de `source` desde já — rejeitado
  por abrir um valor para uma integração que ainda não existe no código.
- Tornar `room_number` obrigatório — rejeitado por quebrar a importação de
  reservas futuras sem quarto definido.
- Definir um padrão fixo de formato para `reservation_code` — rejeitado por
  restringir códigos vindos de fontes ainda não implementadas.

**Justificativa geral:** manter o MVP simples e não travar regras para
cenários (Opera Cloud) que ainda não têm código correspondente.

## [2026-07-30] Campos em aberto do model VipPlan

**Contexto:** o data-model.md definia a tabela VipPlan, mas deixava em
aberto a obrigatoriedade de vários campos, a possibilidade de unicidade
entre reservation_id e planned_date, e os valores de status/delivery_status.

**Decisão:**
- Todos os campos sem ressalva explícita no documento (`reservation_id`,
  `planned_date`, `status`, `delivery_status`, `created_by_id`,
  `created_at`, `updated_at`) são obrigatórios (nullable=False).
  `room_number_override`, `delivered_at` e `delivered_by_id` seguem
  opcionais, como já estava explícito no documento.
- Não haverá unicidade entre `reservation_id` e `planned_date`. Um mesmo
  dia de uma reserva pode ter mais de um VipPlan (ex: chegada e
  aniversário coincidindo na mesma data).
- `status` e `delivery_status` permanecem como texto livre nesta fase,
  reafirmando a decisão de 23/07. Serão fechados quando as telas de
  planejamento existirem.
- O comportamento de `delivered_at`/`delivered_by_id` ao reverter uma
  entrega fica em aberto para quando a funcionalidade de
  marcar/desmarcar entrega for implementada — não bloqueia a criação
  do model agora.

**Alternativas consideradas:**
- Travar unicidade reservation_id+planned_date — rejeitado por poder
  bloquear planejamentos legítimos de dois eventos no mesmo dia.
- Fechar valores de status/delivery_status agora — rejeitado por
  contrariar a decisão de 23/07, que previa esperar as telas existirem.

**Justificativa geral:** priorizar flexibilidade operacional (permitir
mais planejamento do que bloquear) e manter consistência com decisões
já tomadas anteriormente.

## [2026-07-30] Campos em aberto do model VipItem

**Contexto:** o data-model.md definia a tabela VipItem, mas deixava em
aberto a obrigatoriedade de alguns campos (especialmente `cost`), a
precisão do campo `cost`, os valores de `availability_status`, e o
comportamento de "substituição" de um item.

**Decisão:**
- Obrigatórios: `vip_plan_id`, `description`, `responsible_id`,
  `availability_status`, `created_at`, `updated_at`.
- `cost` é opcional (nullable=True). Itens costumam ser planejados antes
  de o custo estar fechado.
- `cost` usa o tipo `Numeric(10, 2)` — nunca `Float`, para evitar erros de
  arredondamento em valores monetários.
- `availability_status` permanece como texto livre nesta fase, seguindo o
  mesmo padrão adotado em `VipPlan.status`. Será fechado quando as telas
  existirem.
- Não haverá campo de entrega por item (`delivery_status` só existe no
  VipPlan) — reafirmando a decisão de 23/07 de que a confirmação de
  entrega é feita em conjunto, não item por item.
- Quando um item é marcado como "substituído", o registro existente é
  editado (não se cria um novo VipItem vinculado). A rastreabilidade da
  informação anterior fica a cargo de uma entrada manual no AuditLog
  (Opção A, já decidida), registrada no momento da edição.
- Comportamento de cascata ao apagar um VipPlan (o que acontece com seus
  VipItems) fica em aberto — nenhuma regra de `ondelete` será definida
  agora. Será decidido quando a funcionalidade de cancelar/apagar um
  planejamento for desenhada, respeitando a regra geral de nunca apagar
  informação sem rastro.

**Alternativas consideradas:**
- Tornar `cost` obrigatório — rejeitado por não refletir a rotina real de
  planejamento antes da cotação de custos.
- Criar um campo `replaced_by_id` para rastrear substituições via um novo
  registro — rejeitado por adicionar complexidade não prevista no
  documento original; o AuditLog manual já cobre a rastreabilidade.

**Justificativa geral:** manter consistência com as decisões já tomadas
para Reservation e VipPlan, e não travar regras de negócio (cascata,
valores de status) que ainda não têm o contexto de tela necessário.

## [2026-07-30] Campos e regras do model AuditLog

**Contexto:** o data-model.md definia a tabela AuditLog com um relacionamento
polimórfico (entity_type + entity_id), e deixava em aberto a obrigatoriedade
dos campos, o escopo de entidades auditadas, e a garantia de imutabilidade.

**Decisão:**
- Todos os sete campos são obrigatórios: `user_id`, `entity_type`,
  `entity_id`, `action`, `details`, `timestamp`.
- `entity_id` é um inteiro comum, sem foreign key e sem relationship —
  relacionamento polimórfico, integridade garantida pelo código da
  aplicação, não pelo banco.
- `details` usa o tipo `Text` (sem limite de tamanho), para não truncar
  descrições de mudança.
- `action` permanece como texto livre nesta fase, mesmo padrão dos demais
  campos de status.
- `entity_type` aceita, desde já, `"Reservation"` como valor válido, além
  de `"VipPlan"` e `"VipItem"` — alterações em Reservation também geram
  entrada de log a partir de agora.
- Entradas de AuditLog nunca são editadas nem apagadas. Essa regra é
  aplicada tecnicamente via eventos do SQLAlchemy (`before_update` e
  `before_delete`), que bloqueiam essas operações quando feitas através
  do código da aplicação. Limitação conhecida: não protege contra acesso
  direto ao banco por fora da aplicação — proteção completa exigiria
  configuração no nível do banco de dados, fora do escopo do MVP.

**Alternativas consideradas:**
- Deixar Reservation fora do escopo do MVP — descartado a pedido do
  usuário; Reservation entra no escopo de auditoria desde já.
- Só documentar a regra de imutabilidade sem aplicá-la no código —
  descartado; a trava técnica foi priorizada mesmo sabendo de sua
  limitação contra acesso direto ao banco.

**Justificativa geral:** priorizar rastreabilidade forte desde o início,
mesmo que exija uma técnica nova (eventos do SQLAlchemy) não usada nos
models anteriores.

Nota adicional: a proteção via listeners (before_update/before_delete) não
cobre um "flask db downgrade" desta migração, pois um DROP TABLE via
Alembic opera no nível do schema, sem passar pelos eventos do SQLAlchemy.
Ou seja, reverter esta migração apaga todo o histórico de auditoria sem
passar pela trava. Aceitável no MVP (tabela nova, sem dados reais em
risco); revisitar se algum dia for necessário reverter esta migração com
dados de produção existentes.

## [2026-08-02] Importação manual de reservas via Opera Cloud (Trilha 1)

**Contexto:** Definido o desenho da primeira importação real de dados,
a partir do relatório RES_DETAIL do Opera Cloud (formato XML).

**Decisões:**
- Formato de importação: XML do relatório RES_DETAIL do Opera Cloud.
- Chave de upsert de Reservation: reservation_code (mapeado de
  CONFIRMATION_NO no XML).
- Reserva nova no arquivo: criada normalmente.
- Reserva existente com dados alterados no Opera: campos vindos do
  Opera são atualizados, mas a configuração manual da reserva
  (planejamentos de vipagem já criados) é preservada. Um aviso visual
  deve indicar que a reserva mudou desde a última importação (mecanismo
  exato definido na etapa de UI).
- Reserva cancelada no Opera: identificada por SHORT_RESV_STATUS = CXL
  no arquivo reimportado. Marcada como cancelada, nunca apagada.
- Sem trava de data: qualquer data futura presente no arquivo pode ser
  importada a qualquer momento.
- Identificação do hóspede (Guest): pelo campo opera_guest_id (mapeado
  de GUEST_NAME_ID no XML), único por perfil do Opera. Cada perfil do
  Opera gera um Guest próprio nesta fase — sem unificação automática de
  perfis duplicados (ver épico de resolução de identidade registrado em
  backlog.md).
- Guest.all_member / all_card_number: derivados dos MEMBERSHIP_TYPE
  presentes na reserva. Considerados apenas tipos iniciados com "A" (A1
  a A5); tipo "ID" e categorias fora da faixa A (All Signature,
  Explorer, Ibis etc.) são ignorados. Quando há mais de um tipo A,
  usa-se o nível mais alto.
- A categoria VIP do hóspede NÃO é mais um campo de texto escrito por
  esta importação — ela é resolvida pelo sistema de badges, descrito na
  entrada de decisão seguinte, logo abaixo desta.
- Reservation.notes (campo novo, tipo Text): cada RES_COMMENT do XML
  vira um parágrafo dentro deste campo, na ordem em que aparecem.

**Mudanças de schema:** Reservation.notes (Text, opcional);
Guest.opera_guest_id (String, opcional, único quando presente).

**Status:** Aprovado.

## [2026-08-02] Categoria VIP do hóspede vira sistema de badges

**Contexto:** A decisão de 2026-07-23 definia Guest.vip_category como
texto livre único. Durante o desenho da importação via Opera Cloud
(entrada acima), ficou claro que um campo de texto único não suporta
com segurança as regras necessárias de atualização automática parcial
sem risco de apagar texto digitado manualmente. Esta decisão substitui
a de 2026-07-23 nesse ponto específico.

**Decisão:**
- Guest.vip_category (campo de texto único) é REMOVIDO do modelo.
- Nova tabela GuestBadge substitui esse campo: um hóspede pode ter
  vários badges independentes (ex: "Gold", "Habitué", "Aniversário",
  "Colaborador Accor"), cada um com sua própria origem e status.
- Campos de GuestBadge: id, guest_id (FK -> Guest), label (string),
  source (string: "all_tier", "keyword_suggestion", "stay_count" ou
  "manual"), status (string: "active", "suggested" ou "rejected"),
  created_at, updated_at, created_by_id (FK -> User, opcional — nulo
  quando source é automático).
- Guest.vip (booleano) passa a significar: hóspede tem pelo menos um
  GuestBadge com status "active", de qualquer origem ou label.
- Badge de origem "all_tier": criado/atualizado automaticamente pela
  importação quando o hóspede tiver nível ALL A3 (Gold), A4 (Platinum)
  ou A5 (Diamond) — entra direto com status "active". Em upgrade de
  nível, o sistema atualiza o label do badge existente. Em downgrade,
  o sistema nunca rebaixa nem remove automaticamente.
- Badge de origem "keyword_suggestion": quando uma palavra-chave for
  encontrada em Reservation.notes (lista inicial fixa no código:
  "aniversário", "niver", "casamento", "vip", "mimo", "colaborador
  accor", "diretoria accor" — não editável pela equipe nesta fase), o
  sistema cria um GuestBadge com status "suggested". Vira "active" só
  quando um humano aceitar.
- Badge de origem "stay_count": quando o hóspede atingir 5 ou mais
  Reservation vinculadas ao mesmo guest_id, o sistema sugere o badge
  "Habitué" com status "suggested". Limitação conhecida: contagem só
  enxerga reservas do mesmo opera_guest_id — hóspedes com perfis
  duplicados no Opera podem ter contagem subestimada até o épico de
  resolução de identidade ser resolvido.
- Badge de origem "manual": criado, editado e removido livremente pela
  equipe, sem regra automática.
- Sugestão recusada (status "rejected") nunca é apagada nem re-sugerida
  automaticamente depois — fica disponível para reativação manual a
  qualquer momento.
- GuestBadge entra no escopo de auditoria do AuditLog, junto com
  Reservation, VipPlan e VipItem.

**Status:** Aprovado.


\## Pendentes (a decidir em etapas futuras)

\- Estrutura exata de pastas do repositório.

\- Ambiente de hospedagem/deploy (quando sair do uso local).

\- Regras específicas de "repetição indevida de item" (pós-MVP).

\- Regras específicas de controle de estoque (pós-MVP).

\- Detalhes técnicos da integração com Opera Cloud (endpoint, autenticação,

&#x20; formato de dados).

