"""
HEADER_COMMENT_AUTOGEN
FILE: config.py
PURPOSE: App configuration — DB, Security, Mail settings

TIPS: Set all secrets as environment variables on Render.
      MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER are required for forgot-password email.
"""

# config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'replace-this-with-a-secure-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'quiz.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Flask-Mail (SMTP) ──────────────────────────────
    # Set these as environment variables on Render
    MAIL_SERVER   = os.environ.get('MAIL_SERVER')   or 'smtp.gmail.com'
    MAIL_PORT     = int(os.environ.get('MAIL_PORT')  or 587)
    MAIL_USE_TLS  = os.environ.get('MAIL_USE_TLS',  'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # your Gmail address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Gmail App Password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or \
        os.environ.get('MAIL_USERNAME') or 'noreply@quizcraft.com'
