import os
from io import BytesIO

from flask import (
    current_app, request, abort, render_template, flash, send_file
)
import telegram

from .. import bot
from . import main


machine = None


@main.route('/show-fsm')
def show_fsm():
    fsm_graph = BytesIO()
    machine.draw_graph(fsm_graph, prog='dot')
    fsm_graph.seek(0)
    return send_file(fsm_graph, attachment_filename='fsm.png', mimetype='image/png')


@main.route('/hook', methods=['POST'])
def reply():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.adavnce(update)
    return 'ok'
