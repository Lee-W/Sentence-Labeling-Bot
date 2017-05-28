import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import telegram

from config import config


APP_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
APP_STATIC_PATH = os.path.join(APP_ROOT_PATH, 'static')
APP_TEMPLATE_PATH = os.path.join(APP_ROOT_PATH, 'templates')

bot = None
db = SQLAlchemy()
bootstarp = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    global bot

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bot = telegram.Bot(config[config_name].BOT_API_TOKEN)

    db.init_app(app)
    bootstarp.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .systemdesign import system_design as system_design_blurprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(system_design_blurprint, url_prefix='/system-design')

    return app
