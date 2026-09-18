"""
Normalizacao de nomes usada para comparar campos de texto do Opera
Cloud (ex.: SHARE_NAMES x FULL_NAME/FULL_NAME_NO_SHR_IND) em funcoes
de vinculo de reservas.

Tres niveis, do mais simples ao mais agressivo -- logica original
validada em decisao de 2026-09-11, portada aqui a partir do script de
medicao share_names_test.py (fora do repositorio). Nivel 1 inclui,
alem da logica original, remocao de caracteres de formatacao
invisiveis (categoria Unicode "Cf", ex.: WORD JOINER U+2060) -- nao
apenas acentos -- resolvendo a pendencia registrada na decisao de
2026-09-17.
"""

import re
import unicodedata

TITLE_SUFFIXES = [
    "mr.", "mr", "mrs.", "mrs", "ms.", "ms", "dr.", "dr", "miss.", "miss",
]


def normalize_level1(text: str | None) -> str:
    """Remove acentos, caracteres de formatacao invisiveis, caixa, e
    normaliza espacos (inclusive ao redor de virgula)."""
    if text is None:
        return ""
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(
        c for c in decomposed
        if not unicodedata.combining(c) and unicodedata.category(c) != "Cf"
    )
    lowered = stripped.lower()
    collapsed = re.sub(r"\s+", " ", lowered).strip()
    no_space_around_comma = re.sub(r"\s*,\s*", ",", collapsed)
    return no_space_around_comma


def normalize_level2(text: str | None) -> str:
    """Nivel 1 + remove sufixos de tratamento comuns."""
    base = normalize_level1(text)
    parts = base.split(",")
    filtered_parts = [p for p in parts if p not in TITLE_SUFFIXES]
    return ",".join(filtered_parts)


def normalize_level3(text: str | None) -> str:
    """Nivel 2 + reordena 'Sobrenome,Nome' -> 'Nome Sobrenome'."""
    base = normalize_level2(text)
    if "," in base:
        parts = base.split(",")
        first_name = parts[-1].strip()
        last_name = " ".join(p.strip() for p in parts[:-1] if p.strip())
        if first_name and last_name:
            return f"{first_name} {last_name}".strip()
        return (first_name or last_name).strip()
    return base
