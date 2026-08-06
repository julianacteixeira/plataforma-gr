from flask import Flask
from flask_login import login_required, current_user
from config import Config
from app.extensions import db, migrate, login_manager, csrf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    csrf.init_app(app)

    # Importa os models para que o Flask-Migrate saiba que eles existem.
    from app import models  # noqa: F401

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    @app.route("/")
    def hello():
        return "Plataforma de Guest Relations - ambiente funcionando!"

    @app.route("/painel")
    @login_required
    def painel():
        return f"Bem-vindo, {current_user.name}! (rota protegida)"

    @app.cli.command("seed-categories")
    def seed_categories_command():
        """Popula a tabela categories com as 28 categorias de VIP definidas."""
        from app.seeds.categories import run
        criadas, atualizadas = run()
        print(f"Categorias criadas: {criadas}")
        print(f"Categorias atualizadas: {atualizadas}")

    return app