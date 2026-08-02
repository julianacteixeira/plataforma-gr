from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."

    # Importa os models para que o Flask-Migrate saiba que eles existem.
    from app import models  # noqa: F401

    @app.route("/")
    def hello():
        return "Plataforma de Guest Relations - ambiente funcionando!"

    return app