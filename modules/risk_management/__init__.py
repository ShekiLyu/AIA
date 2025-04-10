from flask import Blueprint

risk_blueprint = Blueprint('risk', __name__, url_prefix='/risk')

from . import views