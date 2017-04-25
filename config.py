import os


BASE_DIE = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRAK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    from config_secrets import TOKEN, SECRET_KEY
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DEV_DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIE, 'db.sqlite')
    )


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    TESTING= True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('TEST_DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIE, 'db-test.sqlite')
    )


config = {
    'default': DevelopmentConfig,
    'developmen': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}
