from flask import Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
from . import dashboard, auth, terms, post, user, options, media, ai
