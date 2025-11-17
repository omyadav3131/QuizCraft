"""
HEADER_COMMENT_AUTOGEN
FILE: app\quiz\__init__.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# app/quiz/__init__.py
from flask import Blueprint

quiz_bp = Blueprint('quiz', __name__, template_folder='../templates/quiz')

from . import routes  # noqa: E402,F401
