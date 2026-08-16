\# Backlog — Plataforma de Guest Relations



Legenda: \[ ] pendente · \[x] concluído · (P) requer decisão pendente



\## MVP



\### Fundação

\- \[ ] Estrutura de pastas do projeto

\- \[ ] Repositório Git/GitHub privado configurado

\- \[ ] Ambiente Python local funcionando

\- \[ ] Banco de dados modelado (SQLAlchemy)

\- \[ ] Migrações configuradas (Flask-Migrate)

\- \[ ] Login de usuário (Flask-Login)



\### Reservas e Hóspedes

\- \[ ] Importação manual de reservas via arquivo

\- \[ ] Consulta de reservas

\- \[ ] Consulta de hóspedes

\- \[ ] Marcar reserva/hóspede como VIP

\- \[ ] Registrar categoria de VIP



\### Vipagem

\- \[ ] Criar planejamento de vipagem

\- \[ ] Adicionar itens ao planejamento

\- \[ ] Registrar custo por item

\- \[ ] Registrar responsável por item

\- \[ ] Registrar status de entrega por item

\- \[ ] Status geral do planejamento



\### Confiabilidade

\- \[ ] Histórico de alterações (quem, quando, o quê)

\- \[ ] Validações e restrições no banco de dados

\- \[ ] Uso de transações em operações críticas



\### Relatórios

\- \[ ] Exportação de relatório em XLSX



\### Visual

\- \[ ] Identidade editorial aplicada às telas principais



\## Pós-MVP

\- \[ ] Histórico consolidado por hóspede (itens recebidos em estadias anteriores)

\- \[ ] Regras para evitar repetição indevida de itens

\- \[ ] Controle de estoque de itens de vipagem

\- \[ ] Relatórios avançados (filtros, períodos, por categoria/responsável)

\- \[ ] Permissões por papel de usuário (atendente vs. gerente)

\- \[ ] Refinamento visual completo (microinterações em todas as telas)

- [ ] Padronização de sinalização em reservas (comentários/notes do Opera)

  **Contexto (registrado em 2026-08-12, sessão de planejamento da
  importação Opera Cloud):** durante o desenho das palavras-chave de
  badges automáticas, identificaram-se duas lacunas de comunicação que
  limitam o reconhecimento automático:

  1. A equipe usa formas muito variadas e informais para sinalizar
     pedidos de gerência em comentários de reserva (ex: nomes curtos
     como "Daniel" ou "Nat" em vez de nome completo, sem padrão fixo
     de frase).
  2. Ações criadas pelo time de MICE (Meetings, Incentives,
     Conferences, Exhibitions) frequentemente não chegam ao
     conhecimento da GR com antecedência, e quando aparecem em
     comentário de reserva, vêm com nomes muito variados — sem padrão
     algum, tornando inviável qualquer lista de palavras-chave.

  **Proposta:** um projeto à parte, fora do escopo desta plataforma,
  para acordar com as equipes envolvidas um padrão simples de
  sinalização em comentários do Opera. Ideia inicial levantada pela
  usuária para o caso do MICE: adotar um prefixo fixo como
  **"Ação MICE"** seguido de uma descrição breve, sempre que uma ação
  for criada e afete hóspedes vipados. Isso tornaria o reconhecimento
  automático de badges mais confiável no futuro, sem depender de
  listas extensas e sempre incompletas de variações.

  **Status:** ideia registrada, não iniciada. A usuária pretende
  apresentar este documento à equipe.



\## Integrações Futuras

\- \[ ] Camada de integração isolada com Opera Cloud

\- \[ ] Importação automática de reservas via API do Opera Cloud

\- \[ ] Sincronização automática de hóspedes

\- \[ ] (Avaliar) notificações automáticas de vipagem pendente

