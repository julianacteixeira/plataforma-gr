\# Próximos Passos — Plataforma de Guest Relations



\## Próxima etapa a executar

Implementar o model AuditLog em app/models/audit_log.py, seguindo o mesmo
padrão dos anteriores (um arquivo por tabela, registrado em
app/models/__init__.py), e gerar/aplicar a migração correspondente. É o
último model do desenho de banco do MVP.

Campos previstos em docs/technical/data-model.md: user_id (FK -> User),
entity_type, entity_id, action, details, timestamp.

Antes de codificar, decidir (e registrar no decision-log.md) os pontos
ainda em aberto: os valores aceitos de `action`, a obrigatoriedade de cada
campo, o tamanho de `details`, e se `entity_id` terá chave estrangeira
real ou não — do mesmo modo como foi feito para Reservation, VipPlan e
VipItem nas entradas de 2026-07-30.

Ponto importante de modelagem: o AuditLog aponta para registros de
tabelas diferentes (VipPlan, VipItem, Reservation) através do par
entity_type + entity_id. Isso significa que `entity_id` normalmente NÃO
pode ser uma chave estrangeira comum, porque não aponta para uma única
tabela. Decidir isso explicitamente antes de escrever o model.

Lembrar que o log é alimentado manualmente pelo código (Opção A, decisão
de 2026-07-23): cada função que cria ou altera VipPlan/VipItem também
grava uma entrada aqui. Não há captura automática por eventos do
SQLAlchemy nesta fase. Duas decisões recentes dependem disso funcionar:
a substituição de item (editado no lugar, com rastro no AuditLog) e a
futura reversão de entrega.

Depois do AuditLog, o desenho de banco do MVP está completo e a frente
seguinte é autenticação (Flask-Login).



\## Já concluído nesta frente

- Models User, Guest, Reservation, VipPlan e VipItem implementados, com
  migrações aplicadas.
- Tabelas reservations, vip_plans e vip_items criadas e confirmadas no
  banco local.
- Campos em aberto de Reservation (source, room_number, reservation_code)
  decididos e registrados no decision-log.md em 2026-07-30.
- Campos em aberto de VipPlan (obrigatoriedade, não-unicidade de
  reservation_id + planned_date, status/delivery_status como texto livre
  sem default) decididos e registrados no decision-log.md em 2026-07-30.
- Campos em aberto de VipItem (obrigatoriedade, cost opcional com tipo
  Numeric(10, 2), availability_status como texto livre, substituição por
  edição do registro existente com rastro no AuditLog) decididos e
  registrados no decision-log.md em 2026-07-30.



\## Pontos de atenção a resolver antes de fechar o MVP

Ver detalhes em docs/handoff/current-state.md:

- Padronizar `nullable=False` em created_at/updated_at nos models User,
  Guest e Reservation, para ficarem consistentes com VipPlan e VipItem.
- Definir o comportamento de delivered_at/delivered_by_id ao reverter uma
  entrega, quando a funcionalidade de marcar/desmarcar entrega for
  implementada.
- Definir a regra de cascata ao apagar um VipPlan (o que acontece com os
  VipItems ligados a ele). Nenhum ondelete foi definido nas FKs.



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

