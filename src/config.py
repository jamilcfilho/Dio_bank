import os


class Config:
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY"),
    # Passa o caminho que será criado o banco de dados. É em sqlite para não precisar instalar nenhum outro SGBD
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI"),
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY"),


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = 'dev',
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.sqlite",
    JWT_SECRET_KEY = "super-secret",


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = "test"
    DATABASE_URI = 'sqlite://'
    JWT_SECRET_KEY = "test"
