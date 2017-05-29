from flask import Blueprint

sentence_panel = Blueprint('sentence', __name__)

from . import views
