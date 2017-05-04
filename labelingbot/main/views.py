import os
from io import BytesIO

import ujson
from flask import send_file

from .. import APP_STATIC_PATH, APP_TEMPLATE_PATH, bot
from . import main
from .labelingfsm import LabelingMachine

BOT_CONFIG = os.path.join(APP_STATIC_PATH, 'bot_config/FSM.json')
BOT_TEMPLATE_PATH = os.path.join(APP_TEMPLATE_PATH, 'bot_templates')


machine = None


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


@main.route('/show-fsm', methods=['GET'])
def show_fsm():
    fsm_graph = BytesIO()
    machine.draw_graph(fsm_graph, prog='dot')
    fsm_graph.seek(0)
    return send_file(fsm_graph, attachment_filename='fsm.png', mimetype='image/png')
