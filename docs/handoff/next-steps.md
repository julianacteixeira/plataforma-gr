\# Próximos Passos — Plataforma de Guest Relations



\## Próxima etapa a executar

Criar a rota de login (backend) e a rota de logout, usando login_user()
e logout_user() do Flask-Login, e proteger uma rota de teste com
@login_required para validar o fluxo completo (usuário não autenticado
é redirecionado; usuário autenticado acessa a rota normalmente).

Lembrar que login_manager.login_view = "auth.login" já está configurado
em app/__init__.py, esperando essa rota — sem ela, o redirecionamento de
um usuário não autenticado vai falhar.

Lembrar também que o log é alimentado manualmente pelo código (Opção A,
decisão de 2026-07-23): cada função que cria ou altera VipPlan/VipItem
também grava uma entrada no AuditLog. Não há captura automática nesta
fase, então isso precisa ser escrito à mão em cada rota.



\## Já concluído nesta frente

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

