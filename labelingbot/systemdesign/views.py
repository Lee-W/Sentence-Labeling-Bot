from io import BytesIO

from flask import send_file
from pygraphviz.agraph import AGraph
from eralchemy.main import all_to_intermediary, _intermediary_to_dot

from ..models import db
from ..main.views import machine
from . import system_design


@system_design.route('/er-diagram', methods=['GET'])
def show_er_diagram():
    er_diagram = BytesIO()
    er_diagram.name = 'er_diagram'

    table, relationships = all_to_intermediary(db.Model)
    dot_file = _intermediary_to_dot(table, relationships)
    graph = AGraph().from_string(dot_file)
    graph.draw(er_diagram, prog='dot', format='png')

    er_diagram.seek(0)
    return send_file(er_diagram, attachment_filename='er_diagram.png', mimetype='image/png')


@system_design.route('/fsm', methods=['GET'])
def show_fsm():
    fsm_graph = BytesIO()
    machine.draw_graph(fsm_graph, prog='dot')
    fsm_graph.seek(0)
    return send_file(fsm_graph, attachment_filename='fsm.png', mimetype='image/png')
