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
    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'https')

    # ── Brevo REST API (HTTPS for Render Free Tier) ────
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
    MAIL_SENDER_EMAIL = os.environ.get('MAIL_SENDER_EMAIL') or \
        os.environ.get('MAIL_USERNAME') or 'noreply@quizcraft.com'

    # ── Google OAuth 2.0 (OpenID Connect) ──────────────
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    # ── Flask-Mail (SMTP fallback) ─────────────────────
    # Set these as environment variables on Render
    MAIL_SERVER   = os.environ.get('MAIL_SERVER')   or 'smtp.gmail.com'
    MAIL_PORT     = int(os.environ.get('MAIL_PORT')  or 587)
    MAIL_USE_TLS  = os.environ.get('MAIL_USE_TLS',  'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # your Gmail address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Gmail App Password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or \
        MAIL_SENDER_EMAIL
