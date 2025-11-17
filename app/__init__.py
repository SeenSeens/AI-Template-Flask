import os
from flask import Flask, send_from_directory
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_toastr import Toastr
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_folder='core/static', static_url_path='/static')
app.config.from_object(Config)

# Init Core module
from app.core import init_core
init_core(app)

# Serve uploads files
@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)

# debug
# app.debug = True
# toolbar = DebugToolbarExtension(app)
#
# app.config['TEMPLATES_AUTO_RELOAD'] = True
