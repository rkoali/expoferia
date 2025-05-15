from flask import Blueprint

profesor = Blueprint('profesor', __name__)

from . import routes