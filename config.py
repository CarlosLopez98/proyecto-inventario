from decouple import config

class Config:
    SECRET_KEY = "Estaesunallavesecreta"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///proyecto_inventarios.sqlite3'
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{username}:{password}@{hostname}/{database}'.format(
        username = 'root',
        password = 'admin',
        hostname = 'localhost',
        database = 'nombre_base_datos'
    )
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuracion para el envio de correos
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mail@gmail.com'
    MAIL_PASSWORD = 'clave'
    #MAIL_PASSWORD = config(MAIL_PASSWORD)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///proyecto_inventarios_test.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEST = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'test': TestConfig
}
