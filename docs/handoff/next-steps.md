\# Próximos Passos — Plataforma de Guest Relations



\## Próxima etapa a executar

Implementar o model VipPlan em app/models/vip_plan.py, seguindo o mesmo
padrão de User, Guest e Reservation (um arquivo por tabela, registrado em
app/models/__init__.py), e gerar/aplicar a migração correspondente.

Campos previstos em docs/technical/data-model.md: reservation_id
(FK -> Reservation), planned_date, room_number_override, status,
delivery_status, delivered_at, delivered_by_id (FK -> User),
created_by_id (FK -> User), created_at, updated_at.

Antes de codificar, decidir (e registrar no decision-log.md) os pontos
ainda em aberto: os valores aceitos de `status` e `delivery_status`, e a
obrigatoriedade de cada campo — do mesmo modo como foi feito para
Reservation na entrada de 2026-07-30.

Depois de VipPlan, seguem VipItem e AuditLog, nessa ordem.



\## Já concluído nesta frente

- Models User, Guest e Reservation implementados, com migrações aplicadas.
- Tabela reservations criada e confirmada no banco local.
- Campos em aberto de Reservation (source, room_number, reservation_code)
  decididos e registrados no decision-log.md em 2026-07-30.



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

