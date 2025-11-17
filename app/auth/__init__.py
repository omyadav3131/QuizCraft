"""
HEADER_COMMENT_AUTOGEN
FILE: app\auth\__init__.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

from . import routes
