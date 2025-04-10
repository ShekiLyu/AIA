from flask import Blueprint

position_blueprint = Blueprint('position', __name__, url_prefix='/position')

from . import views