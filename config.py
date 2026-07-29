import os
from dotenv import load_dotenv

# Carrega as variáveis definidas no arquivo .env para dentro do ambiente
load_dotenv()


class Config:
    """Configurações da aplicação, lidas a partir do arquivo .env."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-padrao-insegura")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///plataforma_gr.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False