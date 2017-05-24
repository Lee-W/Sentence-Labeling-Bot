import os

from .base import Config, BASE_DIR


class TestingConfig(Config):
    TESTING = True
    try:
        from .secret import BOT_API_TOKEN, SECRET_KEY
    except ModuleNotFoundError as error:
        print('config_secret does not exist')

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('TEST_DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIR, 'data-test.sqlite')
    )
