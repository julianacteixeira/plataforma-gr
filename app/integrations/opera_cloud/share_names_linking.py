"""
Resolucao de vinculo entre reservas via SHARE_NAMES, para o caso em
que room_number ainda nao foi atribuido.

Decisoes que governam este modulo:
- 2026-09-17: SHARE_NAMES pode ser mecanismo primario de vinculo neste
  caso especifico, restrito a correspondencia exata (nivel 2) e apenas
  quando resolve a um unico candidato; ambiguidade vai para revisao
  manual. SHARE_NAMES nunca e persistido nem vira campo de
  ReservaParseada -- entra aqui como dicionario transiente.
- 2026-09-18 (desenho): busca restrita a reservas sem room_number;
  resolucao por nome individual; reciprocidade obrigatoria.
- 2026-09-18 (estrutura): saida em tres categorias; PendingLink
  carrega o motivo; disputa de candidato joga todos os vinculos
  envolvidos para revisao manual.

Nenhum nome de hospede e retornado por este modulo -- apenas
reservation_code.
"""

from dataclasses import dataclass, field

from app.integrations.opera_cloud.name_normalization import normalize_level2

# Motivos de pendencia (rotulos tecnicos internos, nao exibidos crus
# ao usuario final -- a interface traduz para portugues quando for o
# caso).
REASON_AMBIGUOUS = "ambiguous"
REASON_NO_RECIPROCITY = "no_reciprocity"
REASON_CANDIDATE_CONFLICT = "candidate_conflict"


@dataclass
class ResolvedLink:
    """Vinculo de reservas resolvido automaticamente com seguranca: cada
    nome citado resolveu para 1 candidato, a citacao foi reciproca e
    cada reserva cita todas as demais do vinculo."""
    reservation_codes: list[str]


@dataclass
class PendingLink:
    """Reserva cujo SHARE_NAMES nao pode ser resolvido com seguranca
    automatica -- precisa de revisao manual."""
    reservation_code: str
    reason: str


@dataclass
class ShareNamesResolution:
    resolved: list[ResolvedLink] = field(default_factory=list)
    pending_review: list[PendingLink] = field(default_factory=list)
    without_share_names: list[str] = field(default_factory=list)


def _split_share_names(raw: str | None) -> list[str]:
    """Separa o texto bruto de SHARE_NAMES nos nomes citados.

    Separador "/" confirmado na analise do XML real (decisao de
    2026-09-17). Devolve lista vazia quando nao ha nada util.
    """
    if not raw:
        return []
    return [part.strip() for part in raw.split("/") if part.strip()]


def resolve_share_names_links(
    reservations: list,
    share_names_by_code: dict[str, str | None],
) -> ShareNamesResolution:
    """Resolve vinculos entre reservas sem room_number, via SHARE_NAMES.

    Parametros:
    - reservations: lista de ReservaParseada JA FILTRADA por quem chama,
      contendo apenas reservas com room_number is None. A funcao nao
      refaz esse filtro.
    - share_names_by_code: dicionario transiente
      {reservation_code: texto_bruto_de_SHARE_NAMES}, montado por quem
      chama a partir do XML e descartado logo apos o uso. Nunca
      persistido.

    Devolve ShareNamesResolution com as tres categorias.
    """
    result = ShareNamesResolution()

    # Indice de nome normalizado -> lista de reservation_codes que
    # possuem esse nome. Lista (nao valor unico) porque nomes repetidos
    # entre hospedes diferentes sao possiveis, e e justamente isso que
    # caracteriza ambiguidade.
    codes_by_normalized_name: dict[str, list[str]] = {}
    for reservation in reservations:
        normalized = normalize_level2(reservation.full_name)
        if normalized:
            codes_by_normalized_name.setdefault(normalized, []).append(
                reservation.reservation_code
            )

    # ---------------------------------------------------------------
    # Primeira passagem: resolve cada nome citado individualmente.
    # ---------------------------------------------------------------
    # targets_by_code[A] = {B, C} -- para quem A aponta, ja resolvido.
    targets_by_code: dict[str, set[str]] = {}
    # Reservas que ja falharam nesta passagem, com o motivo.
    failed_by_code: dict[str, str] = {}

    for reservation in reservations:
        code = reservation.reservation_code
        cited_names = _split_share_names(share_names_by_code.get(code))

        if not cited_names:
            result.without_share_names.append(code)
            continue

        targets: set[str] = set()
        failed = False
        for cited_name in cited_names:
            normalized = normalize_level2(cited_name)
            candidates = [
                candidate_code
                for candidate_code in codes_by_normalized_name.get(normalized, [])
                if candidate_code != code  # nunca aponta para si mesma
            ]
            if len(candidates) != 1:
                # 0 candidatos (nao encontrado) ou 2+ (ambiguo) -- em
                # ambos os casos nao ha resolucao segura.
                failed = True
                break
            targets.add(candidates[0])

        if failed:
            failed_by_code[code] = REASON_AMBIGUOUS
        else:
            targets_by_code[code] = targets

    # ---------------------------------------------------------------
    # Segunda passagem: reciprocidade, repetida ate estabilizar.
    # ---------------------------------------------------------------
    # A aponta B so vale se B tambem aponta A. Remover uma reserva
    # pode quebrar a reciprocidade de outra que apontava para ela, por
    # isso a checagem se repete ate uma volta inteira sem remocoes.
    changed = True
    while changed:
        changed = False
        for code in sorted(targets_by_code):
            targets = targets_by_code[code]
            reciprocal = all(
                target in targets_by_code and code in targets_by_code[target]
                for target in targets
            )
            if not reciprocal:
                failed_by_code[code] = REASON_NO_RECIPROCITY
                del targets_by_code[code]
                changed = True

    # ---------------------------------------------------------------
    # Terceira passagem: monta os vinculos por fecho transitivo.
    # ---------------------------------------------------------------
    # Se A<->B e B<->C, o vinculo e {A, B, C}.
    links: list[set[str]] = []
    visited: set[str] = set()
    for code in sorted(targets_by_code):
        if code in visited:
            continue
        link = {code}
        to_visit = [code]
        while to_visit:
            current = to_visit.pop()
            for target in targets_by_code.get(current, set()):
                if target not in link:
                    link.add(target)
                    to_visit.append(target)
        visited.update(link)
        links.append(link)

    # ---------------------------------------------------------------
    # Quarta passagem: disputa de candidato entre vinculos distintos.
    # ---------------------------------------------------------------
    # O fecho transitivo junta num mesmo conjunto tudo que esta ligado.
    # Por isso, quando um candidato e reivindicado por dois vinculos
    # distintos, eles aparecem aqui FUNDIDOS num conjunto so. O sinal
    # da disputa e o conjunto nao ser completo: num vinculo legitimo,
    # cada reserva cita todas as outras do mesmo vinculo. Se alguma
    # reserva nao cita exatamente "todas as demais", o conjunto inteiro
    # vai para revisao manual (decisao de 2026-09-18, estrutura).
    for link in links:
        is_complete = all(
            targets_by_code[code] == link - {code}
            for code in link
        )
        if is_complete:
            result.resolved.append(
                ResolvedLink(reservation_codes=sorted(link))
            )
        else:
            for code in link:
                failed_by_code[code] = REASON_CANDIDATE_CONFLICT

    for code, reason in sorted(failed_by_code.items()):
        result.pending_review.append(
            PendingLink(reservation_code=code, reason=reason)
        )

    return result
