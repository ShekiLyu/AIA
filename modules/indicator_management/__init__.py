from flask import Blueprint

indicator_blueprint = Blueprint('indicator', __name__, url_prefix='/indicator')

from . import views