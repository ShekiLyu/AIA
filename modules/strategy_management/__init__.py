from flask import Blueprint

strategy_blueprint = Blueprint('strategy', __name__, url_prefix='/strategy')

from . import views