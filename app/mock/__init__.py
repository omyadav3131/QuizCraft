from flask import Blueprint

mock_bp = Blueprint('mock', __name__)

from . import routes
