from flask import Blueprint

estudiante = Blueprint('estudiante', __name__)

from . import routes