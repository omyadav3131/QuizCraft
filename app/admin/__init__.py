"""
HEADER_COMMENT_AUTOGEN
FILE: app\admin\__init__.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# app/admin/__init__.py
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

from . import routes
