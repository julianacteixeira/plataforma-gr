from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def set_password(self, password):
        """Gera o hash da senha informada e guarda em password_hash.
        Nunca guardamos a senha em texto puro."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Confere se a senha informada corresponde ao hash guardado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(user_id):
    """Usado pelo Flask-Login para recarregar o usuário logado
    a partir do ID guardado na sessão do navegador."""
    return User.query.get(int(user_id))
