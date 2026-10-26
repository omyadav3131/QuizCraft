"""
HEADER_COMMENT_AUTOGEN
FILE: app\__init__.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail


db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address, default_limits=[])
mail = Mail()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    migrate = Migrate(app, db)

    # Apply ProxyFix for Render reverse proxy (ensures https scheme and real client IP)
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


    # Register blueprints
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.quiz import quiz_bp
    from app.competition import competition_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(competition_bp, url_prefix='/competition')

    # Public routes
    from flask import render_template
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/terms')
    def terms():
        return render_template('terms.html')

    # ── Custom error handlers ──────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    return app
