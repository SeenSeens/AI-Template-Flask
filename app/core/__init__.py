# app/core/__init__.py

import os
from logging.handlers import TimedRotatingFileHandler
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def init_core(app):
    """Khởi tạo phần core của ứng dụng Flask"""

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Cấu hình login
    login_manager.login_view = "admin.login"

    # Import models để migrate
    from app.core import models  # noqa

    print("[DEBUG] Loaded models:", db.metadata.tables.keys())

    # Cấu hình media folder
    media_folder = os.path.join(app.root_path, '..', 'uploads')
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    app.config['MEDIA_FOLDER'] = media_folder
    app.config['MEDIA_URL'] = '/uploads/'

    # Cài đặt logging
    configure_logging(app)

    # Đăng ký các Blueprint
    from app.core.routes.main import main
    from app.core.routes.admin import admin_bp
    from app.core.routes.api import api_bp

    app.register_blueprint(main)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

def configure_logging(app):
    """Cấu hình ghi log"""
    handler = TimedRotatingFileHandler('flask-template.log', when='midnight', interval=1, backupCount=10)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
