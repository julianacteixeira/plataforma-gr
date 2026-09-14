"""
Fatia 4a — Detecção de categorias por palavra-chave em notas de reserva.

Função de leitura (consulta CategoryKeyword/Category para comparação),
mas não grava nada no banco. Não decide para qual reserva o badge vai
(isso é a Fatia 4b) e não cria StayBadge (isso é a Fatia 4c).
"""

import unicodedata

from app.extensions import db
from app.models.category import Category
from app.models.category_keyword import CategoryKeyword

ATENCAO_ESPECIAL_NAME = "Atenção Especial"


def _normalize(text):
    """Remove acentuação e converte para minúsculo, para comparação.

    Decisão de 2026-09-14 (decision-log.md): usa unicodedata da
    biblioteca padrão do Python, sem dependência nova.
    """
    if text is None:
        return ""
    decomposed = unicodedata.normalize("NFKD", text)
    without_accents = "".join(
        char for char in decomposed if not unicodedata.combining(char)
    )
    return without_accents.lower()


def _keyword_matches(normalized_note_text, normalized_keyword):
    """Aplica a regra de combinação '+': todos os termos separados por
    '+' precisam aparecer no texto da nota para a keyword bater
    (decisão de 2026-08-12, item 10)."""
    parts = [part.strip() for part in normalized_keyword.split("+")]
    parts = [part for part in parts if part]
    return all(part in normalized_note_text for part in parts)


def detect_categories_in_notes(notes):
    """Recebe uma lista de ReservationNote (de uma única reserva) e
    devolve uma lista de detecções, uma por combinação (nota, categoria)
    que bateu.

    Cada item devolvido é um dicionário:
        {
            "category_id": int,
            "matched_keyword": str,    # texto exato da keyword cadastrada
            "matched_note_type": str,  # comment_type da nota de origem
        }

    Regras aplicadas (decision-log.md, 2026-09-12):
    - item 3: busca por nota individual, não texto concatenado da reserva.
    - item 4: sem filtro de comment_type (varre GEN e todos os outros).
    - item 5: descarte de "Atenção Especial" avaliado nota a nota.
    - 2026-09-14: normalização ignora acento e caixa.

    Pode haver mais de uma detecção para a mesma categoria (keywords
    diferentes batendo em notas diferentes, ou até na mesma nota) — a
    responsabilidade de evitar duplicidade de StayBadge é da Fatia 4c,
    não desta função.
    """
    active_keywords = (
        db.session.query(CategoryKeyword)
        .join(Category, CategoryKeyword.category_id == Category.id)
        .filter(CategoryKeyword.active.is_(True))
        .filter(Category.active.is_(True))
        .all()
    )

    atencao_especial = (
        db.session.query(Category)
        .filter(Category.name == ATENCAO_ESPECIAL_NAME)
        .first()
    )
    atencao_especial_id = atencao_especial.id if atencao_especial else None

    detections = []

    for note in notes:
        normalized_note_text = _normalize(note.text)
        note_matches = []

        for category_keyword in active_keywords:
            normalized_keyword = _normalize(category_keyword.keyword)
            if _keyword_matches(normalized_note_text, normalized_keyword):
                note_matches.append(
                    {
                        "category_id": category_keyword.category_id,
                        "matched_keyword": category_keyword.keyword,
                        "matched_note_type": note.comment_type,
                    }
                )

        # Descarte de Atenção Especial: só se, NESTA nota, houver mais de
        # uma categoria detectada (Atenção Especial + outra).
        categories_in_note = {match["category_id"] for match in note_matches}
        if atencao_especial_id in categories_in_note and len(categories_in_note) > 1:
            note_matches = [
                match
                for match in note_matches
                if match["category_id"] != atencao_especial_id
            ]

        detections.extend(note_matches)

    return detections
