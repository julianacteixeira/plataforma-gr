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


\## [2026-08-03] Decisões técnicas da implementação da importação Opera Cloud

**Contexto:** ao planejar a implementação da importação manual de reservas
(decisão de 2026-08-02), surgiram três pontos técnicos sem decisão prévia
registrada: onde guardar o arquivo XML enviado, onde ficar o módulo de
integração, e se o campo `Guest.vip_category` deveria ser removido agora.

**Decisão:**
- O arquivo XML enviado no upload é processado em memória e descartado
  após a importação — não é salvo em disco. A rastreabilidade do que foi
  criado/alterado fica no AuditLog, não no arquivo original.
- O módulo de integração com o Opera Cloud fica isolado em
  `app/integrations/opera_cloud/`, conforme a decisão de 2026-07-13 de
  manter essa integração separada do restante do sistema. O nome
  genérico `integrations` (em vez de `imports`) deixa a pasta pronta para
  outras integrações externas futuras, não só o Opera.
- `Guest.vip_category` é removido do model agora (não apenas depreciado),
  já que a tabela `guests` está vazia (sem dados reais em risco) e a
  decisão de 2026-08-02 já havia aprovado sua substituição por
  `GuestBadge`.

**Status:** Aprovado.

## [2026-08-03] Revisão de escopo: GuestBadge, campos de contato, ItemType e templates de sugestão

**Contexto:** revisão de funcionalidades feita com a usuária, comparando o
pedido original com uma aplicação anterior (descartada) do mesmo domínio.
O objetivo foi levantar funcionalidades reais da rotina de GR ainda não
cobertas pelo modelo de dados atual. Código da aplicação anterior não foi
reutilizado em nenhum momento — apenas comportamento funcional e imagens
de interface serviram de referência.

**Decisões:**

1. **GuestBadge precisa ser revisado para separar badges por evento
   (ligados à estadia) de badges por hóspede (persistentes).** Badges de
   ocasião pontual (Aniversário, Lua de Mel, Romântico, Pacote, Fechamento,
   Pedido de Desculpas) devem ficar ligados à reserva/estadia específica
   (Reservation ou VipPlan), não ao Guest — do contrário, apareceriam
   permanentemente em estadias futuras do mesmo hóspede, o que não reflete
   a realidade. Badges de nível de fidelidade ou relação institucional
   (Gold, Platinum, Diamond, ALL Signature, Colaborador Accor, Influencer,
   Diretoria, Investidor) continuam ligados ao Guest, pois persistem entre
   estadias. Esta decisão revisa a estrutura de GuestBadge aprovada em
   2026-08-02 e substitui aquele desenho neste ponto específico.

2. **Vínculo manual de perfis duplicados de hóspede entra no MVP**, como
   tabela simples de vínculo entre dois registros de Guest (ex:
   `hospede_principal_id` / `hospede_secundario_id`). A detecção
   automática por similaridade de nome permanece pós-MVP (já registrada
   como pendência em 2026-08-02).

3. **Novos campos no MVP:**
   - Guest: telefone e e-mail (opcionais), com aviso de dado sensível
     (LGPD) na interface e função de exclusão desses dois campos
     especificamente, sem apagar o restante do cadastro.
   - Reservation: ETA confirmado manualmente (formato HH:MM, distinto do
     ETA vindo do Opera Cloud); status de contato prévio (enum: pendente,
     contatado, sem_resposta, confirmado).
   - VipItem: categorização de custo (ex: "A&B" ou "Brindes"), necessária
     para os relatórios financeiros do painel principal.

4. **Nova entidade ItemType (cadastro leve de tipo de item).** Ao
   registrar, num VipPlan, um item que nunca foi usado em nenhuma
   vipagem anterior, o sistema deve solicitar o cadastro completo do
   item antes de permitir seu uso: nome, custo padrão, e instrução de
   montagem (texto livre, tipo "ficha técnica" — como o item deve ser
   posicionado, se precisa de talher/guardanapo/taça etc.). Itens já
   cadastrados ficam disponíveis para reaproveitamento em vipagens
   futuras. VipItem passa a referenciar um ItemType, em vez de manter
   `description` como texto totalmente livre. Esta é uma versão
   simplificada do módulo "Catálogo" mencionado como pós-MVP — o
   catálogo visual completo (fotos, checklist estruturado de montagem,
   organização visual) permanece pós-MVP; o cadastro funcional mínimo
   entra agora.

5. **Campo Group (faixa 1–6) por categoria/badge**, representando nível
   de custo/importância para visão gerencial futura (aproximação de
   faixa de valor esperado por vipagem). Este campo é independente da
   prioridade de sugestão de item (item 6, abaixo) e não deve ser usado
   para decidir qual item sugerir.

6. **Campo de prioridade de sugestão, por categoria (não por Group).**
   Quando uma estadia se qualifica para mais de uma categoria/badge
   simultaneamente, o sistema sugere automaticamente apenas o template de
   item da categoria de maior prioridade nesse ranking — nunca a soma
   automática de templates de categorias diferentes. A equipe pode
   adicionar itens manualmente por cima da sugestão a qualquer momento.
   Prioridade é definida caso a caso pela equipe (ex: Aniversário e
   ALL Signature/All Kids tendem a prioridade alta, por serem
   compromissos indispensáveis; outras categorias podem ter prioridade
   mais baixa), sem relação fixa com o valor de Group.

7. **Template de item por categoria, com variação binária por presença
   de criança na reserva** (tem criança / não tem criança — nunca
   escalona pela quantidade). A variação correta é aplicada
   automaticamente na sugestão inicial do VipPlan; ajustes finos (ex:
   um item por criança quando há mais de uma) são feitos manualmente
   pela equipe depois da sugestão.

**Impacto no trabalho já implementado:** o model GuestBadge, migrado com
sucesso em 2026-08-03 (migração 6ac2cc539f41), precisa ser revisado antes
do início do módulo de importação Opera Cloud (Etapa 2 do plano de
2026-08-03), por conta da decisão 1 acima. A tabela guest_badges está
vazia (nenhum dado real), então a revisão de schema não tem risco de
perda de informação.

**Status:** Aprovado.

## [2026-08-03] Desenho revisado de schema: Category, ItemType, StayBadge, GuestLink

**Contexto:** decorrente da entrada de decisão anterior deste mesmo dia
("Revisão de escopo: GuestBadge, campos de contato, ItemType e templates
de sugestão"), esta entrada fecha o desenho técnico das tabelas
envolvidas, revisado em conjunto antes de qualquer implementação.

**Decisões:**

1. **Nova tabela Category**, substituindo o uso de texto livre como
   categoria: `id`, `name`, `scope` ("guest" ou "stay"), `group_number`
   (1 a 6, faixa de custo/importância), `suggestion_priority` (inteiro,
   independente do group_number), `active` (boolean).

2. **GuestBadge revisado** (migração de 2026-08-03, tabela ainda vazia,
   revisão sem risco de perda de dado): troca o campo `label` (texto
   livre) por `category_id` (FK → Category, restrito a categorias com
   scope = "guest"). Mantém `source`, `status`, `created_by_id`,
   `created_at`, `updated_at` como já estava.

3. **Nova tabela StayBadge**, para categorias de evento (scope = "stay"):
   `id`, `reservation_id` (FK → Reservation — não VipPlan, para preservar
   o histórico agregado da estadia inteira mesmo quando há múltiplos
   VipPlans na mesma reserva), `category_id`, `source`
   ("keyword_suggestion" ou "manual"), `status` ("active", "suggested",
   "rejected"), `created_by_id`, `created_at`, `updated_at`.

4. **Nova tabela ItemType** (cadastro leve e reaproveitável de item):
   `id`, `name` (único), `default_cost` (Numeric 10,2), `cost_category`
   ("A&B", "Brindes" ou "Papelaria"), `assembly_instructions` (text),
   `created_at`, `updated_at`. Ao cadastrar um item nunca antes usado
   durante o preenchimento de um VipPlan, o sistema pergunta se deve
   vinculá-lo imediatamente a uma Category (criando um
   CategoryItemTemplate) ou deixá-lo solto, podendo ser incluído em um
   template posteriormente.

5. **Nova tabela CategoryItemTemplate**: `id`, `category_id` (FK →
   Category), `item_type_id` (FK → ItemType), `requires_child` (boolean,
   nullable — null significa indiferente à presença de criança; true/false
   distingue a variação do item conforme presença de criança na reserva,
   nunca por quantidade).

6. **VipItem ajustado**: adiciona `item_type_id` (FK → ItemType,
   obrigatório). O campo `description` deixa de ser o nome do item e
   passa a ser opcional, reservado para observação específica daquela
   instância do item na vipagem (ex: "sem açúcar"), sem duplicar o nome
   já registrado em ItemType.

7. **Nova tabela GuestLink** (vínculo manual de perfis duplicados):
   `primary_guest_id` (FK → Guest), `secondary_guest_id` (FK → Guest),
   `created_by_id` (FK → User), `created_at`.

8. **Campos novos em tabelas existentes:**
   - Reservation: `confirmed_eta` (string, formato HH:MM, opcional),
     `contact_status` (string, default "pendente").

   Nota de correção (2026-08-03): a versão original deste item também
   listava `phone` e `email` como campos novos em Guest — redundante,
   pois os dois já existem no model desde o início do projeto (nenhuma
   mudança de schema necessária ali). O que de fato é novo é
   comportamento de interface, ainda pendente (ver pendência abaixo, na
   seção "Pendentes"), não uma mudança de schema.

**Status:** Aprovado.

## [2026-08-06] Fechamento definitivo: Category — scope, grupo, prioridade, always_apply, manual_only

**Contexto:** conclusão da revisão de Category iniciada em 2026-08-03, que
ficou pendente em next-steps.md. Fecha as últimas classificações em aberto
(scope de 4 categorias, grupo de IBIOBI/Habitué, correção de tier do IBIOBI)
e formaliza dois campos booleanos novos no model Category.

**Novos campos em Category:**
- `always_apply` (boolean, default False): quando True, a categoria soma
  itens automaticamente com todas as outras always_apply presentes na
  mesma sugestão, ignorando completamente o ranking normal de
  suggestion_priority. Categorias always_apply nunca competem entre si.
- `manual_only` (boolean, default False): quando True, a categoria nunca
  entra automaticamente na sugestão (nem via always_apply, nem via
  ranking normal) — só aparece se a equipe a ativar manualmente naquele
  VipPlan específico. Seu suggestion_priority, quando existir, serve
  apenas para posicionamento visual na tela, sem efeito na lógica
  automática.

**Regra de interação consolidada:**
1. Se qualquer categoria always_apply=True estiver presente, o sistema
   soma os itens de todas as always_apply presentes e ignora o ranking
   normal, exceto por adições manuais feitas pela equipe.
2. Se nenhuma always_apply estiver presente, o sistema usa o ranking
   normal (suggestion_priority 1-21); só a categoria de maior prioridade
   entre as presentes vence — as demais não aparecem automaticamente.
3. Categorias manual_only=True nunca entram nos passos 1 ou 2.

**Correção de classificação: IBIOBI sai do grupo always_apply.**
Levantamento inicial listava IBIOBI entre as 7 categorias sempre-
-prioritárias. Revisão com a usuária mostrou que não há gasto padrão
associado a hóspedes IBIOBI (clube de fidelidade Senpar/TS Itu já envia
os brindes prontos; a atuação do GR é só entrega, já que esses hóspedes
não têm acesso a quartos). Além disso, reservas IBIOBI não vêm do
relatório padrão de importação — chegam por planilha separada do clube
de fidelidade, recebida 2+ vezes por semana. Sem gatilho automático
possível (nem keyword, nem badge de import) e sem gasto padrão a somar,
IBIOBI é reclassificado como manual_only. O tier always_apply passa de
7 para 6 categorias.

**Scope definido para as 4 categorias pendentes:**
- Atenção Especial → stay. Categoria genérica para motivos de vipagem
  sinalizados nas notes da reserva que não justificam categoria própria.
  Não persiste entre estadias.
- Pax Querido → guest, manual_only. Significa que o pax é querido da
  equipe (relação pessoal, não institucional) — persiste entre
  hospedagens do mesmo hóspede, mas nunca entra automaticamente no
  planejamento; exige ativação manual em cada estadia específica.
- Convidados Gerência → stay. Reserva pedida por alguém da gerência.
  Fonte majoritariamente manual — notes têm sinalização muito variável,
  não compensa tentar keyword_suggestion aqui.
- Voucher Novos Colaboradores → stay, always_apply, grupo 7. Ligado à
  chegada específica do colaborador novo, não à pessoa em si. Template
  de item já levantado: carta nominal, necessaire Coca-Cola, voucher
  tirolesa, gift drink (podendo incluir cartinha à mão dos colegas).

**Festa Junina não vira categoria própria.** Cai dentro de Ações
(already always_apply): sempre que houver VIP solicitado pela equipe de
MICE/Marketing/etc., sem sugestão automática de itens (acordo pontual
caso a caso).

**Habitué/Habituée:** entra como badge normalmente (source stay_count,
sugerido a partir de 5+ reservas do mesmo opera_guest_id), disputa
suggestion_priority = 2 no ranking normal, grupo 8 (mesmo grupo de
Ações). Nunca terá CategoryItemTemplate vinculado — quando vence a
disputa, a lista de sugestão fica intencionalmente vazia, forçando
preenchimento manual pela equipe (esses hóspedes já recebem muito ao
longo do relacionamento com o hotel, então cada vipagem é avaliada caso
a caso).

**suggestion_priority passa a ser nullable=True** (migração aea187b152c4).
Categorias always_apply não têm posição no ranking — ficam com o campo
vazio (None), refletindo que a competição por prioridade simplesmente
não se aplica a elas, em vez de usar um valor numérico sentinela sem
sentido.

**Palavras-chave adicionais confirmadas** (complementam a lista fixa
inicial da decisão de 2026-08-02, futuramente migradas para
CategoryKeyword):
- "prever mimo", "prever vip", "vip", "mimo" → Atenção Especial, MAS
  apenas quando não acompanhadas de outra palavra-chave mais específica
  na mesma nota (ex: "Aniversário da Solange dia 06/08 - prever mimo
  simbólico" deve casar com Aniversário, não Atenção Especial).
- "lua de mel", "romântico", "romantico" → Comemorações (não vira
  categoria própria "Lua de Mel/Romântico" para fins de keyword; a
  categoria Lua de Mel/Romântico permanece no ranking com
  suggestion_priority=12 para os casos identificados manualmente, mas a
  detecção automática por keyword aponta para Comemorações).

**Tabela final de categorias (28 no total: 6 always_apply, 2
manual_only, 20 no ranking normal 1-21) — scope, grupo, always_apply,
manual_only, suggestion_priority:** ver tabela consolidada em
docs/technical/data-model.md (atualização pendente, próxima etapa) e
no histórico de conversa da sessão de fechamento.

**Migração aplicada:** aea187b152c4 (revises 730b36ea5422), 2026-08-06.
Cria category_keywords; adiciona always_apply e manual_only a
categories; altera suggestion_priority para nullable.

**Status:** Aprovado.

## [2026-08-06] Mudança confirmada: fim do estoque físico próprio de itens de vipagem

**Contexto:** a usuária confirmou que, em até 10 dias a partir desta
data, deixará de manter estoque físico próprio dos itens usados em
vipagens. Os itens passarão a ficar centralizados numa loja física do
hotel, e a equipe de GR precisará fazer requisições semanais por
memorando — processo já existente e familiar, similar ao que já é
feito hoje para pedidos de A&B.

**Impacto no produto:** planejamento antecipado e preciso passa a ser
ainda mais crítico do que já era, já que decisões de vipagem agora
alimentam diretamente um processo formal de requisição, não apenas um
controle interno de custo.

**Decisões tomadas nesta entrada:**
- `ItemType.cost_category` (já existente: "A&B", "Brindes", "Papelaria")
  permanece necessário — usado tanto para métricas ao Comitê quanto
  como possível campo de agrupamento no futuro relatório de requisição.
- Novo item de backlog: relatório de requisição semanal em XLSX,
  filtrável por período (data inicial/final), somando a quantidade de
  cada item planejado no intervalo — para virar a base do memorando de
  requisição à loja física. Detalhes de agrupamento (por item, por
  cost_category, ou ambos) e de quais status de VipPlan/VipItem entram
  na contagem ficam para a sessão de desenho de fluxo/UX em andamento.
- Identificada possível necessidade de um segundo status em VipPlan,
  distinguindo "planejamento sem conflito de estoque, pronto para
  entrega assim que o quarto estiver disponível" de "efetivamente
  entregue" — hoje o modelo só tem `delivery_status`. Não decidido
  ainda; aguarda resultado da sessão de UX em andamento antes de
  qualquer mudança de schema.

**Não é uma decisão de schema ainda** — só registro de contexto de
negócio confirmado e dos itens de backlog/pendência que essa mudança
gera. Mudanças em VipPlan/VipItem/ItemType, se necessárias, serão
decididas depois do resultado da sessão de UX.

**Status:** Aprovado (registro de contexto). Pendências geradas por
esta decisão aguardam fluxo de UX.

## [2026-08-06] Decisões técnicas derivadas da entrevista de fluxo/UX

**Contexto:** sessão de entrevista de UX (fora deste ambiente) desenhou
em texto o fluxo principal de telas do sistema (Chegadas, Guests in
House, Home, Planejamento de Vipagem, Requisição Semanal, Perfil do
Hóspede, Catálogo/Pacotes). Esta entrada registra apenas as decisões
com implicação direta em schema, levantadas durante a revisão técnica
desse resultado. As decisões puramente visuais/de fluxo ficam
registradas em docs/design/design-system.md e
docs/design/approved-ui-notes.md; a lista de novas telas e
funcionalidades fica registrada em docs/product/backlog.md.

**Decisões:**

1. **Novo campo `VipPlan.ready_for_delivery`** (boolean, default False).
   Representa o toggle "Tudo pronto" da seção "VIPs do dia" — um
   checkpoint de revisão diária, distinto de `delivery_status` (que
   continua controlando a confirmação real de entrega via botão
   "Marcar como entregue", só habilitado depois que
   ready_for_delivery = True). O toggle desliga automaticamente a cada
   edição feita no VipPlan após já estar ligado, forçando nova revisão
   humana. Comportamento de rota, a implementar na fase técnica; cada
   desligamento automático deve gerar entrada em AuditLog.

2. **Sistema de Requisição Semanal usa vínculo explícito, não
   comparação de datas.** Cada VipItem incluído numa requisição recebe
   um `requisition_id` (FK, nullable) no momento em que a requisição é
   gerada — não apenas uma comparação de timestamps. A condição
   "aguardando próxima requisição" (exibida como contador na Home) é
   avaliada **por cost_category** (A&B, Brindes e Papelaria têm
   frequência de pedido diferente, portanto requisições e contadores
   são independentes por categoria). Detalhamento completo do model
   WeeklyRequisition fica para a migração dedicada a essa
   funcionalidade.

3. **Pacote tem preço padrão editável por venda.** `Package.default_price`
   existe no cadastro do Pacote; o valor efetivamente cobrado é
   registrado por venda (em uma tabela própria de venda/registro,
   detalhada na migração dedicada a Catálogo/Pacotes) e pode divergir
   do padrão.

4. **Anotações livres da equipe (post-its da Home) persistem no
   banco**, em tabela simples (sem necessidade de campos estruturados
   além de conteúdo e autoria), visíveis para toda a equipe (não
   individuais), e permanecem até serem excluídas manualmente. A
   redação original da entrevista ("sem necessidade de estrutura de
   banco de dados") foi esclarecida nesta revisão como referindo-se à
   ausência de complexidade de modelo, não à ausência de persistência.

5. **Nova tabela `InstitutionalDate`** para marcações do mini-calendário
   da Home (feriados, reuniões, fechamentos do resort — eventos
   institucionais, não eventos de hóspede/VipPlan). Campos: id, date,
   name, color, created_by_id, created_at. Sem campo de descrição
   longa, por decisão de manter a marcação só visual.

6. **Novo campo `Guest.preferences`** (texto livre), seguindo o mesmo
   padrão já usado em campos ainda não estruturados do projeto (ex:
   Reservation.notes).

**Escopo novo identificado, ainda sem detalhamento técnico completo**
(a receber migração e entrada de decisão própria em sessão futura):
- Tela "Guests in House" (não implica schema novo — é uma visão sobre
  Reservation já existente, filtrada por check_in < hoje <= ETD do
  check_out).
- Sistema de Catálogo/Pacotes completo (Package, PackageItemTemplate,
  registro de venda).
- Sistema de Requisição Semanal completo (WeeklyRequisition).

**Status:** Aprovado.

## [2026-08-12] Modelo de dados do Memorando (substitui WeeklyRequisition)

**Contexto:** sessão de planejamento dedicada, motivada pela transição do
estoque físico de itens de vipagem para requisição formal na loja do
hotel. Partiu da análise da rotina real de memorandos (exemplos reais em
PDF/XLSX da pasta `23. MEMORANDO` do OneDrive, sem dados reais de
hóspede mantidos neste documento) antes de qualquer desenho técnico.

**Decisões:**

1. **Nome definitivo: `Memorando`.** O nome provisório `WeeklyRequisition`
   é abandonado. Não existe período fixo (semanal ou outro) embutido no
   nome nem na estrutura — o período coberto por cada memorando é
   escolhido no momento da geração, não é uma regra do sistema. Loja
   entra como mais um setor de destino possível, não como um processo à
   parte.

2. **Dois tipos de Memorando, mesma tabela, campo `tipo` distingue:**
   - **Tipo A ("consolidado"):** agrega itens de vários VipPlans
     diferentes, filtrados por setor de preparo + data de entrega (ex:
     "Cozinha, 11/08"). Corresponde aos memorandos VIP Cozinha, VIP
     Confeitaria, A&B do dia a dia.
   - **Tipo B ("pacote"):** sempre vinculado a exatamente um `VipPlan`
     (nunca agrupa mais de um). Usado para bolos e pacotes contratados
     (Kit Festa, Pacote Romântico etc.), que exigem campos adicionais de
     venda. Um memorando Tipo B pode conter linhas de mais de um setor
     dentro do mesmo documento (ex: Confeitaria e A&B juntos, como no Kit
     Festa).
   - Decisão tomada por medo concreto de perda de rastreabilidade caso um
     único memorando combinasse itens de VipPlans diferentes no Tipo B:
     risco de a confeitaria descartar o memorando após entregar um item
     e "perder" outro pacote que estivesse no mesmo documento, ou de
     duplicar a entrega de um item já feito.

3. **Tabela `Memorando` (cabeçalho):**
   - `id`
   - `tipo` ("consolidado" ou "pacote")
   - `vip_plan_id` — obrigatório apenas quando `tipo = "pacote"`; nulo em
     "consolidado"
   - `version_number` — inteiro, começa em 1
   - `previous_version_id` — FK para a versão anterior da mesma
     "linhagem" de memorando; nulo na v1. Nenhuma versão é apagada.
   - `status_versao` — indica se esta é a versão vigente ou se foi
     "substituída" por uma versão mais nova. Versões substituídas
     continuam no banco (nunca apagadas) mas só aparecem nas telas
     quando o histórico é explicitamente consultado; por padrão, o
     sistema mostra apenas a versão vigente de cada linhagem.
   - `responsavel_interno_id` (FK → User) — quem assume a
     responsabilidade pelo conteúdo do memorando perante o setor
     executor. Campo do CONTEÚDO do documento, editável livremente
     enquanto o memorando não foi exportado. Pode ser uma pessoa
     diferente de quem operou o sistema (ex: alguém pede para Juliana
     gerar um memorando do qual outra pessoa da equipe será a
     responsável).
   - `generated_by_id` (FK → User), `generated_at` — METADADO técnico de
     auditoria (quem operou o sistema e quando), nunca aparece no
     arquivo exportado, nunca editável.
   - `data_pedido`
   - `observacao` (texto livre — ex: "lançar na CI VIP Hospedagem - VIP
     FAMÍLIA BAUDUCCO")
   - `exported_at` — nulo até a primeira exportação; uma vez preenchido,
     TODO o conteúdo do memorando (incluindo `responsavel_interno_id`)
     vira imutável. Qualquer mudança de conteúdo após a exportação exige
     gerar uma nova versão (v+1), nunca editar a versão exportada.
   - Campos exclusivos de `tipo = "pacote"` (nulos em "consolidado"):
     `forma_pagamento`, `valor_total`, `pax_adultos`,
     `pax_criancas_6_12`, `pax_criancas_ate_5`.
   - `forma_pagamento`: texto livre nesta fase (mesmo padrão adotado para
     outros campos de status controlado no projeto), com quatro valores
     válidos já identificados pela usuária: "Pagamento antecipado"
     (cobrado com a Juliana ou com Reservas, antes do lançamento),
     "Pagamento no checkout" (cobrado no front desk, na saída, após
     lançamento), "Cortesia" (cobrança interna na CI VIP Hospedagem),
     "Faturamento IBIOBI" (cobrança na Conta Master do Clube de Férias
     IBIOBI, fechamento semanal). Observação registrada para o futuro
     (não bloqueia esta decisão): "Cortesia" e "Faturamento IBIOBI"
     apontam para centros de custo diferentes; se um dia for necessário
     relatório segmentado por centro de custo, pode valer a pena um
     campo próprio `centro_de_custo` — avaliar quando a necessidade for
     concreta.

4. **Tabela `MemorandoLine` (linhas), nova:**
   - `id`, `memorando_id` (FK)
   - `vip_item_id` — nulo quando a linha for um item avulso/de sobra,
     sem vínculo a nenhum VipPlan (buffer para momentos de correria);
     preenchido quando a linha vem de um VipItem real e existente.
   - `item_type_id` — sempre preenchido, mesmo em linha vinculada a um
     VipItem, para facilitar consulta e agrupamento sem precisar navegar
     até o VipItem de origem.
   - `quantidade`
   - `data_entrega` — campo PRÓPRIO da linha, independente do
     `planned_date` do VipPlan de origem. Motivo: itens perecíveis
     costumam ser pedidos para entrega no mesmo dia do uso, enquanto
     outros itens podem ser pedidos com antecedência e guardados.
   - `horario` (opcional)
   - `pax` (opcional, sempre digitado manualmente — nunca puxado
     automaticamente da Reservation, pois pode divergir do número de
     hóspedes da reserva, ex: festas com convidados externos)
   - `descricao_observacao` (texto livre da linha, ex: "montar na Sala
     4")
   - Uma linha vinculada a um VipItem preserva, em cada versão gerada, a
     lista exata de VipItems que compunham aquele total no momento da
     geração — isto é o que permite reconstruir, meses depois, por que
     uma quantidade específica foi pedida (ex: "por que pedimos 9
     tábuas e não 8"), mesmo que um dos VipPlans de origem tenha sido
     alterado ou cancelado posteriormente.

5. **Novo campo em `ItemType`: `preparation_sector`.** Valores
   identificados: Cozinha, Confeitaria, A&B (Restaurante/Bares — setor
   físico do hotel, não confundir com a `cost_category` "A&B" que é
   classificação interna de custo), Recepção, Loja. É este campo — e não
   um campo repetido no cabeçalho do Memorando — que determina o setor
   de cada linha, permitindo que um único Memorando Tipo B agregue
   linhas de setores diferentes no mesmo documento.

6. **Exportação e trava de edição.** O sistema não substitui a pasta do
   OneDrive como destino final — a usuária continua exportando o
   arquivo (Excel/PDF) para lá manualmente. O que muda: (a) o sistema
   registra internamente quando e por quem cada versão foi gerada
   (`generated_by_id`/`generated_at`); (b) o arquivo exportado sai
   travado — somente leitura, editável apenas pelo usuário da usuária —
   para impedir o comportamento observado hoje de outras pessoas
   pesquisarem "memorando" no Explorer e sobrescreverem o primeiro
   arquivo encontrado. Dentro do sistema, "editar" nunca significa
   alterar um memorando já exportado — significa gerar uma nova versão,
   recalculada a partir do estado atual dos VipPlans, preservando a
   versão anterior intacta no histórico.

**Pendência registrada para a fase de implementação (não bloqueia o
fechamento desta sessão):** a formatação exata do arquivo exportado
(layout, cores, larguras de coluna, fontes) deve seguir o padrão visual
já em uso nos modelos reais da usuária (Memorando VIP Cozinha, VIP
Confeitaria, A&B, Bolo/Kit Festa). Essa decisão será tomada durante a
implementação, com os arquivos originais como referência direta, e não
neste documento.

**Alternativas consideradas:**
- Guardar no Memorando apenas o resultado agregado (sem apontar para os
  VipItems de origem, linha a linha) — rejeitado por quebrar a
  rastreabilidade granular que é princípio central do projeto.
- Permitir que um Memorando Tipo B agrupe itens de mais de um VipPlan —
  rejeitado pelo risco concreto de perda ou duplicidade de entrega
  relatado pela usuária.
- Tratar a Loja como um fluxo de requisição separado do Memorando comum
  — rejeitado; Loja é apenas mais um valor de `preparation_sector`.

**Status:** Aprovado.


## Pendentes (a decidir em etapas futuras)

\- Tela de perfil do hóspede (pós-MVP): exibir aviso visual de dado
  sensível/LGPD ao lado dos campos `phone` e `email` de Guest, e
  oferecer uma função específica que apaga apenas esses dois campos,
  sem afetar o restante do cadastro. Não exige migração — os campos já
  existem no model.

\- Estrutura exata de pastas do repositório.

\- Ambiente de hospedagem/deploy (quando sair do uso local).

\- Regras específicas de "repetição indevida de item" (pós-MVP).

\- Regras específicas de controle de estoque (pós-MVP).

\- Detalhes técnicos da integração com Opera Cloud (endpoint, autenticação,

&#x20; formato de dados).

