import os
import logging
from flask import Flask, send_from_directory
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_toastr import Toastr
from config import Config
from logging.handlers import TimedRotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(Config)

# Khởi tạo SQLAlchemy và Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app.models import * # Import models để chúng có thể được phát hiện bởi Flask-Migrate
print("[DEBUG] Loaded models:", db.metadata.tables.keys())

login_manager = LoginManager(app)
login_manager.login_view = "admin.login"  # Redirects unauthorized users to the login page

csrf = CSRFProtect(app)

# Configuration for media files
app.config['MEDIA_FOLDER'] = 'media'

# Configures the logging
def configure_logging(app):
    # Create a file handler which logs even debug messages
    handler = TimedRotatingFileHandler('flask-template.log', when='midnight', interval=1, backupCount=10)
    handler.setLevel(logging.INFO)  # Set the log level you want here
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

configure_logging(app)

from app.routes.main import main as main_blueprint
app.register_blueprint(main_blueprint)

from app.routes.admin import admin_bp
app.register_blueprint(admin_bp)

from app.routes.api import api_bp
app.register_blueprint(api_bp)

# debug
app.debug = True
toolbar = DebugToolbarExtension(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
