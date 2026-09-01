# Referência de Campos do Opera Cloud — Relatório RES_DETAIL

Status: documento vivo. Diferente do decision-log.md (que registra decisões
tomadas), este arquivo registra FATOS OBSERVADOS sobre o comportamento real
do relatório RES_DETAIL e da interface do Opera Cloud. Deve ser atualizado
diretamente, sem necessidade de nova entrada no decision-log, sempre que um
fato novo for confirmado. Nenhuma informação aqui contém dado de hóspede —
apenas nomes de campos, códigos e suas descrições.

## Comentários de reserva (RES_COMMENT_TYPE)

### Tipos disponíveis na interface (tela "Notes" > "Search and Select Type")

| Código | Descrição na interface |
|---|---|
| GEN | GEN |
| GENERAL | GENERAL |
| GUEST_REQUEST | GUEST_REQUEST |
| HSK | HOUSEKEEPING |
| RESERVATION | RESERVATION |
| GIFT | GIFT |
| OCC | Ocorrencias |
| PREF | Preference notes |
| REC | Reception |
| RES | Reservation |
| FB | F&B NOTES |

### ATENÇÃO — o código exportado no relatório NÃO é o mesmo da interface

Confirmado por comparação direta, em 2026-08-28, entre notas reais visíveis
na interface e o XML RES_DETAIL exportado da mesma reserva: o campo
RES_COMMENT_TYPE do relatório usa um dicionário de códigos DIFERENTE do
campo Type mostrado na tela de Notes.

Mapeamento confirmado até agora (incompleto, sujeito a expansão):

| Código no relatório (RES_COMMENT_TYPE) | Tipo(s) confirmado(s) na interface |
|---|---|
| RES | RESERVATION |
| CAS | OCC (Occorrencias) e GIFT — confirmado incluir pelo menos estes dois; pode incluir mais, ainda não mapeado |
| GEN | Não totalmente mapeado — no arquivo de amostra analisado, teve título tanto "GENERAL" quanto "RESERVATION", sugerindo que também pode agregar mais de um tipo de interface |

**Regra de uso, enquanto este mapeamento estiver incompleto:** nenhuma
lógica do sistema deve presumir o significado de um RES_COMMENT_TYPE pelo
nome do código. O código é tratado como opaco pelo parser (decisão de
2026-08-12, mantida). Este mapeamento é só para consulta humana ao revisar
dados, não para lógica automática.

**Como atualizar esta tabela:** ao identificar na interface o Type real de
uma nota cujo RES_COMMENT_TYPE já se conhece no relatório, adicionar ou
completar a linha correspondente acima. Não precisa de aprovação nem
decision-log — é registro de fato observado.

## Campo Título (RES_COMMENT_DESCRIPTION)

Campo obrigatório e independente do Type na interface (tela "Notes"),
correspondendo à tag RES_COMMENT_DESCRIPTION no relatório. Confirmado, por
análise estatística de um arquivo real (698 reservas, 1608 comentários,
2026-08-28), que este campo VARIA de forma independente do tipo — o mesmo
RES_COMMENT_TYPE pode ter títulos diferentes. Não é redundante com o tipo;
carrega informação própria.

Valores observados até agora: GENERAL, IN HOUSE, RESERVATION.

## Campo CF_NOTE_DESC — confirmado como redundante, não utilizado

Presente no relatório, mas confirmado (2026-08-28, mesma análise estatística
acima) como espelho do campo Título (RES_COMMENT_DESCRIPTION), idêntico em
99,4% dos casos analisados (1599 de 1608), vazio nos demais (quando Título =
"IN HOUSE"). Não carrega informação adicional. Não utilizado no MVP.

## Traces internos (G_DEPT_ID)

### Estrutura confirmada (2026-08-28, comparação com XML real)

| Tag | Papel |
|---|---|
| DEPT_ID | Código do departamento (ver tabela abaixo) |
| GTV_TRACE_ON | Data do trace, formato DD/MM/AA |
| TRACE_TEXT | Texto livre do trace |
| RESV_NAME_ID1 | Identificador interno de reserva (não usado — mesmo ID se repete em todos os traces da mesma reserva) |

Isso resolve a lacuna de campo registrada em decision-log.md, 2026-08-12,
item 6, que previa o formato `[DEPT_ID - data] texto` sem confirmar os
nomes exatos das tags de origem.

### Códigos de departamento (trace) confirmados na interface

| Código | Descrição |
|---|---|
| ACC | Accounts |
| AMG | Assistant Manager |
| BAG | Bagagiste |
| BAR | Bar |
| BQT | Banquet |
| CON | Concierge |
| ECI | Early Check-In |
| ECI_A | Early Check-In Accepted |
| ECI_R | Early Check-In Refused |
| F&B | Restaurant |
| FB | Restaurant |
| FIT | So FIT |
| GST | Guest Relations |
| HSK | Housekeeping |
| KIT | Kitchen |
| MAI | Maintenance |
| MAN | General Manager |
| PMS | Default Department |
| REC | Reception |
| REM | Opera Remote - Wireless User |
| RES | Reservations |
| RES 2 | Restaurant 2 |
| RES1 | Restaurant 1 |
| RES2 | Restaurant 2 |
| RMS | Room Service |
| SAL | Sales |
| SPA | So SPA |
| STC | Skip The Clean |
| STC_APP | Skip The Clean by guest |
| TBR | To Be Reviewed |
| WAR | Warning Traces |
