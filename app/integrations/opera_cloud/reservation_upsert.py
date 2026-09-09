"""
Upsert de Reservation e ReservationNote a partir de dados extraidos do
XML RES_DETAIL (Fatia 3 da Frente 3 - Opera Cloud).

Reaproveita upsert_guest (Fatia 2) para resolver/criar o Guest antes de
gravar a Reservation. Nao faz commit/rollback -- add()/flush() apenas,
mesma regra das fatias anteriores (Opcao B, decisao de 2026-08-24: uma
transacao por reserva, decidida na orquestracao/Fatia 5).
"""

from datetime import date, datetime

from app.extensions import db
from app.models import Reservation, ReservationNote
from app.integrations.opera_cloud.parser import ReservaParseada
from app.integrations.opera_cloud.guest_upsert import upsert_guest


def _parse_data_trunc(texto: str) -> date | None:
    """TRUNC_BEGIN/TRUNC_END, formato DD-MON-AA (ex: 07-SEP-26)."""
    try:
        return datetime.strptime(texto.title(), "%d-%b-%y").date()
    except ValueError:
        return None


def _parse_data_curta(texto: str) -> date | None:
    """ARRIVAL/DEPARTURE, formato DD/MM/AA (ex: 07/09/26)."""
    try:
        return datetime.strptime(texto, "%d/%m/%y").date()
    except ValueError:
        return None


def _formatar_dept_traces(traces) -> str | None:
    """
    Um paragrafo por trace, formato "[DEPT_ID - data] texto" (decisao
    de 2026-08-12, item 6). Nunca gera placeholder vazio -- None
    quando nao ha traces.
    """
    if not traces:
        return None
    linhas = [f"[{t.dept_id} - {t.data}] {t.texto}" for t in traces]
    return "\n\n".join(linhas)


def upsert_reservation(reserva: ReservaParseada) -> tuple[Reservation | None, str | None]:
    """
    Cria ou atualiza uma Reservation e recria (delete-and-recreate) suas
    ReservationNote a partir de uma ReservaParseada.

    Devolve (Reservation, None) em caso de sucesso, ou (None,
    mensagem_de_erro) em caso de falha -- quem chama (orquestracao,
    Fatia 5) usa a mensagem para gravar ImportErrorRecord.error_message.

    Regras aplicadas, todas de decisoes ja registradas:
    - Chave de upsert: reservation_code (decisao de 2026-08-02).
    - TRUNC_BEGIN/END sao a fonte primaria de check_in/check_out;
      ARRIVAL/DEPARTURE servem so para conferencia. Divergencia vira
      erro, reserva nao e gravada (decisao de 2026-08-26).
    - Reserva sem opera_guest_id vira erro (upsert_guest devolve None).
    - Quando o opera_guest_id resolvido diverge do guest_id ja gravado
      nesta Reservation (mudanca de titularidade), o vinculo e
      atualizado e uma ReservationNote de sistema (comment_type=
      "SISTEMA") registra a mudanca (decisao de 2026-09-08).
    - is_shared, adults, children, room_number, opera_status, rate_code
      sao sempre sobrescritos pelo valor mais recente do Opera.
    - dept_traces e recalculado por inteiro a cada importacao.
    - ReservationNote: delete-and-recreate a cada importacao (decisao
      de 2026-08-26, decorrente da ausencia de identificador estavel
      por comentario) -- EXCETO notas de sistema (comment_type=
      "SISTEMA"), que sao preservadas entre importacoes para manter o
      rastro de mudancas de titularidade ao longo do tempo (decisao de
      2026-09-08).
    """
    check_in = _parse_data_trunc(reserva.check_in)
    check_out = _parse_data_trunc(reserva.check_out)
    arrival = _parse_data_curta(reserva.arrival_check)
    departure = _parse_data_curta(reserva.departure_check)

    if None in (check_in, check_out, arrival, departure):
        return None, (
            f"Reserva {reserva.reservation_code}: falha ao interpretar "
            f"datas (check_in={reserva.check_in!r}, "
            f"check_out={reserva.check_out!r}, "
            f"arrival={reserva.arrival_check!r}, "
            f"departure={reserva.departure_check!r})."
        )

    if check_in != arrival or check_out != departure:
        return None, (
            f"Reserva {reserva.reservation_code}: TRUNC_BEGIN/END "
            f"diverge de ARRIVAL/DEPARTURE (check_in={check_in} vs "
            f"arrival={arrival}; check_out={check_out} vs "
            f"departure={departure})."
        )

    guest = upsert_guest(reserva)
    if guest is None:
        return None, (
            f"Reserva {reserva.reservation_code}: sem opera_guest_id "
            f"(GUEST_NAME_ID ausente ou vazio)."
        )

    reservation = Reservation.query.filter_by(
        reservation_code=reserva.reservation_code
    ).first()

    guest_id_anterior = None
    nome_guest_anterior = None
    if reservation is not None:
        guest_id_anterior = reservation.guest_id
        if guest_id_anterior != guest.id and reservation.guest is not None:
            nome_guest_anterior = reservation.guest.full_name

    if reservation is None:
        reservation = Reservation(
            reservation_code=reserva.reservation_code,
            source="opera_cloud",
        )
        db.session.add(reservation)

    reservation.guest = guest
    reservation.check_in = check_in
    reservation.check_out = check_out
    reservation.room_number = reserva.room_number
    reservation.opera_status = reserva.opera_status
    reservation.is_shared = reserva.is_shared
    reservation.adults = reserva.adults
    reservation.children = reserva.children
    reservation.rate_code = reserva.rate_code
    reservation.dept_traces = _formatar_dept_traces(reserva.traces)

    db.session.flush()

    ReservationNote.query.filter(
        ReservationNote.reservation_id == reservation.id,
        ReservationNote.comment_type != "SISTEMA",
    ).delete(synchronize_session=False)

    for comentario in reserva.comments:
        db.session.add(
            ReservationNote(
                reservation_id=reservation.id,
                comment_type=comentario.comment_type,
                title=comentario.title,
                order_by=comentario.order_by,
                text=comentario.text,
            )
        )

    if guest_id_anterior is not None and guest_id_anterior != guest.id:
        identificador_anterior = nome_guest_anterior or f"guest_id {guest_id_anterior}"
        maior_ordem_comentarios = max((c.order_by for c in reserva.comments), default=0)
        maior_ordem_sistema = db.session.query(
            db.func.max(ReservationNote.order_by)
        ).filter(
            ReservationNote.reservation_id == reservation.id,
            ReservationNote.comment_type == "SISTEMA",
        ).scalar() or 0
        maior_ordem = max(maior_ordem_comentarios, maior_ordem_sistema)
        db.session.add(
            ReservationNote(
                reservation_id=reservation.id,
                comment_type="SISTEMA",
                title=None,
                order_by=maior_ordem + 1,
                text=(
                    f"Titularidade da reserva alterada: de "
                    f"'{identificador_anterior}' para '{guest.full_name}'."
                ),
            )
        )

    db.session.flush()
    return reservation, None
