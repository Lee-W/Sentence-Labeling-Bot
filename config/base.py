import os


BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BOT_API_TOKEN = os.environ.get('BOT_API_TOKEN')
    WEB_HOOK_URL = os.environ.get('WEB_HOOK_URL')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass
