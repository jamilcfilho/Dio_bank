import os
import click
from datetime import datetime

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Integer, String, func, ForeignKey, Boolean
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()

# Criando uma 'role' de usuários 'admin' e 'user'


class Role(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"


# Criação de tabelas = 'User'


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

# Criação de tabelas = 'Post'


class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    created: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    # User fica em minúsculo devido que é o __tablename__ que a classe User recebe. Se ela ainda fosse por exemplo: UserPost, nesse caso seria chamada através de 'user_post' (nada em maiúsculo e ainda coloca-se a separação com o underline)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"


@click.command('init-db')
def init_db_command():
    # Limpa os dados exixtentes e cria novas tabelas
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Inicializando o banco de dados.')


# Por convenção sempre é chamado de 'create_app', é a classe que configura o app da aplicação
def create_app(test_config=None):
    # Criando e configurando o 'app'
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Passa o caminho que será criado o banco de dados. É em sqlite para não precisar instalar nenhum outro SGBD
        SQLALCHEMY_DATABASE_URI="sqlite:///blog.sqlite",
        JWT_SECRET_KEY="super-secret",
    )

    if test_config is None:
        # Carrega a configuração da instância, se existir
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carrega a configuração do teste se for aprovado
        app.config.from_mapping(test_config)

    # Garantindo que a pasta da instância exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Registrando o comando 'cli' do click
    app.cli.add_command(init_db_command)

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
