"""
HEADER_COMMENT_AUTOGEN
FILE: main.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# main.py
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Bind to 127.0.0.1 for local-only access.
    # In production use a proper WSGI server (gunicorn) and secure configuration.
    app.run(debug=True, host='127.0.0.1', port=5000)
