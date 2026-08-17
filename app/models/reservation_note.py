from app.extensions import db


class ReservationNote(db.Model):
    __tablename__ = "reservation_notes"

    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(
        db.Integer, db.ForeignKey("reservations.id"), nullable=False
    )
    comment_type = db.Column(db.String(20), nullable=False)
    order_by = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ReservationNote {self.id} {self.comment_type}>"
