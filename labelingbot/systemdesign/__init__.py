from flask import Blueprint

system_design = Blueprint('system-design', __name__)

from . import views
