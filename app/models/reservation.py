from datetime import datetime, timezone
from app.extensions import db


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    room_number = db.Column(db.String(20), nullable=True)
    reservation_code = db.Column(db.String(50), unique=True, nullable=False)
    source = db.Column(db.String(20), nullable=False, default="manual")
    notes = db.Column(db.Text, nullable=True)
    confirmed_eta = db.Column(db.String(5), nullable=True)
    contact_status = db.Column(db.String(20), nullable=False, default="pendente")
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Reservation {self.reservation_code}>"
