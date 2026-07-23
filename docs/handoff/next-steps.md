\# Próximos Passos — Plataforma de Guest Relations



\## Próxima etapa a executar

Implementar o modelo de dados aprovado (docs/technical/data-model.md) como models SQLAlchemy dentro da aplicação Flask, seguido da configuração do Flask-Migrate. Começar pela estrutura de pastas da aplicação (organização em módulos), depois models simples (User, Guest) antes dos mais complexos.





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

