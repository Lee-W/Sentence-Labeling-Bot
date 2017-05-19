import os

import ujson
from flask import render_template, request
import telegram

from .. import (
    APP_STATIC_PATH, APP_TEMPLATE_PATH,
    bot
)
from . import main
from .labelingfsm import LabelingMachine

BOT_CONFIG = os.path.join(APP_STATIC_PATH, 'bot_config/FSM.json')
BOT_TEMPLATE_PATH = os.path.join(APP_TEMPLATE_PATH, 'bot_templates')


machine = None

bot.set_webhook()

def init_machine():
    global machine

    with open(BOT_CONFIG, 'r') as config_file:
        data = ujson.load(config_file)
        states = data['states']
        transitions = data['transitions']

    machine = LabelingMachine(
        states=states,
        transitions=transitions,
        initial_state='user',
        bot_client=bot,
        template_path=BOT_TEMPLATE_PATH,
    )

init_machine()


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/reply', methods=['POST'])
def reply():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'
