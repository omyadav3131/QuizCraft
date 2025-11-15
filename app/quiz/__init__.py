# app/quiz/__init__.py
from flask import Blueprint

quiz_bp = Blueprint('quiz', __name__, template_folder='../templates/quiz')

from . import routes  # noqa: E402,F401
