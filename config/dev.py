import os

from .base import Config, BASE_DIR


class DevelopmentConfig(Config):
    DEBUG = True
    try:
        from .secret import BOT_API_TOKEN, SECRET_KEY
    except ModuleNotFoundError as error:
        print('Some secret config variables does not set')

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DEV_DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
    )
