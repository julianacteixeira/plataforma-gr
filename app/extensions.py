from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instâncias únicas, compartilhadas por toda a aplicação.
# São criadas aqui "vazias" e conectadas à aplicação de verdade
# dentro da função create_app() (em app/__init__.py).
db = SQLAlchemy()
migrate = Migrate()