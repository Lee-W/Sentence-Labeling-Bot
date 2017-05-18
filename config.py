import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BOT_API_TOKEN = os.environ.get('BOT_API_TOKEN')
    SQLALCHEMY_COMMINT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    try:
        from config_secret import BOT_API_TOKEN, SECRET_KEY
    except ModuleNotFoundError as error:
        print('config_secret does not exist')

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DEV_DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
    )


class TestingConfig(Config):
    TESTING = True
    try:
        from config_secret import BOT_API_TOKEN, SECRET_KEY
    except ModuleNotFoundError as error:
        print('config_secret does not exist')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('TEST_DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIR, 'data-test.sqlite')
    )


class ProducionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
    )


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prodution': ProducionConfig
}
