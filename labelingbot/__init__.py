import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import telegram

from config import config


APP_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
APP_STATIC_PATH = os.path.join(APP_ROOT_PATH, 'static')
APP_TEMPLATE_PATH = os.path.join(APP_ROOT_PATH, 'templates')

bot = None

db = SQLAlchemy()
bootstarp = Bootstrap()
migrate = Migrate()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def setup_bot(api_token, webhook_url):
    global bot

    bot = telegram.Bot(api_token)
    bot.set_webhook(webhook_url)


def create_app(config_name):
    app = Flask(__name__)
    current_config = config[config_name]
    app.config.from_object(current_config)
    current_config.init_app(app)

    setup_bot(current_config.BOT_API_TOKEN, current_config.WEB_HOOK_URL)

    db.init_app(app)
    bootstarp.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .systemdesign import system_design as system_design_blueprint
    from .sentence_panel import sentence_panel as sentence_panel_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(system_design_blueprint, url_prefix='/system-design')
    app.register_blueprint(sentence_panel_blueprint, url_prefix='/panel')

    return app
