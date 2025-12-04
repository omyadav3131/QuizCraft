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
    # Bind to 0.0.0.0 so the app is reachable from other devices on the LAN.
    # In production use a proper WSGI server (gunicorn) and secure configuration.
    app.run(debug=True, host='0.0.0.0', port=5000)
