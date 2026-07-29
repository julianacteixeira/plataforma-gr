from flask import Flask
from config import Config
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Importa os models para que o Flask-Migrate saiba que eles existem.
    from app import models  # noqa: F401

    @app.route("/")
    def hello():
        return "Plataforma de Guest Relations - ambiente funcionando!"

    return app