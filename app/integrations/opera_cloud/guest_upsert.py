"""
Upsert de Guest a partir de dados extraidos do XML RES_DETAIL
(Fatia 2 da Frente 3 - Opera Cloud).

Este modulo cuida SO dos campos crus de Guest (full_name, all_member,
all_card_number, pmid). NAO cria GuestBadge (fatia propria, decidida
separadamente) e NAO decide commit/rollback -- isso e responsabilidade
da orquestracao (Fatia 5), ja que cada reserva tem sua propria
transacao (decisao de 2026-08-24, "Opcao B").
"""

from app.extensions import db
from app.models import Guest
from app.integrations.opera_cloud.parser import ReservaParseada, MembershipParseado


NIVEIS_ALL_VALIDOS = {"A1", "A2", "A3", "A4", "A5", "A6"}


def _maior_nivel_all(memberships: list[MembershipParseado]) -> MembershipParseado | None:
    """
    Filtra memberships por tipos A1-A6 (decisao de 2026-08-02, estendida
    para A6 em 2026-08-16) e devolve o de maior nivel. Tipos "ID" e
    qualquer outro fora da faixa (ex: "G7") sao ignorados.
    """
    candidatos = [m for m in memberships if m.membership_type in NIVEIS_ALL_VALIDOS]
    if not candidatos:
        return None
    return max(candidatos, key=lambda m: int(m.membership_type[1]))


def upsert_guest(reserva: ReservaParseada) -> Guest | None:
    """
    Cria ou atualiza um Guest a partir de uma ReservaParseada.

    Devolve None quando a reserva nao tem opera_guest_id -- quem chama
    (orquestracao, Fatia 5) decide registrar isso como ImportErrorRecord.

    Nao faz commit nem rollback -- so add()/flush(), para o Guest.id
    ficar disponivel para a Reservation (Fatia 3) usar como FK dentro da
    mesma transacao da reserva.
    """
    if not reserva.opera_guest_id:
        return None

    guest = Guest.query.filter_by(opera_guest_id=reserva.opera_guest_id).first()

    if guest is None:
        guest = Guest(opera_guest_id=reserva.opera_guest_id)
        db.session.add(guest)

    guest.full_name = reserva.full_name

    nivel = _maior_nivel_all(reserva.memberships)
    if nivel is not None:
        guest.all_member = True
        guest.all_card_number = nivel.membership_card_no

        cartao = nivel.membership_card_no
        if cartao and len(cartao) == 16 and not guest.pmid:
            guest.pmid = cartao[7:15]
    # Se a reserva nao trouxer nenhuma fidelidade A1-A6, preserva o que
    # ja existia em all_member/all_card_number/pmid (decisao: nunca
    # apaga informacao sem rastro).

    db.session.flush()
    return guest
