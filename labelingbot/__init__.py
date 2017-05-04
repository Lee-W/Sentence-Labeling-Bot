import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import telegram

from config import config


APP_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
APP_STATIC_PATH = os.path.join(APP_ROOT_PATH, 'static')
APP_TEMPLATE_PATH = os.path.join(APP_ROOT_PATH, 'template')

bot = None
db = SQLAlchemy()


def create_app(config_name):
    global bot

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bot = telegram.Bot(config[config_name].BOT_API_TOKEN)

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
