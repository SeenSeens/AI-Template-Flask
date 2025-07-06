import hashlib
from app import db, login_manager
from app.models.users import User

@login_manager.user_loader
def load_user(user_id):
    # return None
    return User.query.get(int(user_id))