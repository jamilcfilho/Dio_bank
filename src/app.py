import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.models import db

migrate = Migrate()
jwt = JWTManager()

# Por convenção sempre é chamado de 'create_app', é a classe que configura o app da aplicação


def create_app(environment="production"):
    # Criando e configurando o 'app'
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")

    # Garantindo que a pasta da instância exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializando a extensão 'app'
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Registrando a Blueprint
    from src.controllers import user
    from src.controllers import auth
    from src.controllers import role

    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app
