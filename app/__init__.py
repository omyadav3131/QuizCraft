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


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)


    # Register blueprints
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.quiz import quiz_bp
    from app.competition import competition_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(competition_bp, url_prefix='/competition')

    # home route
    from flask import render_template
    @app.route('/')
    def home():
        return render_template('home.html')

    return app
