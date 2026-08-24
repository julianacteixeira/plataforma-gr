from datetime import datetime, timezone
from app.extensions import db


class ImportErrorRecord(db.Model):
    __tablename__ = "import_errors"

    id = db.Column(db.Integer, primary_key=True)
    import_log_id = db.Column(
        db.Integer, db.ForeignKey("import_logs.id"), nullable=False, index=True
    )
    confirmation_no = db.Column(db.String(50), nullable=False)
    error_message = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    import_log = db.relationship("ImportLog")

    def __repr__(self):
        return f"<ImportErrorRecord {self.id} import_log_id={self.import_log_id}>"
