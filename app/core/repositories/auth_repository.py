import hashlib
from app.core import db
from app.core.models import User
from .base_repository import BaseRepository

class AuthRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, username):
        return self.model.query.filter_by(username=username.strip()).first()

    def register_user(self, username, email, password, **kwargs):
        hashed_pw = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
        user = User(
            username=username.strip(),
            email=email.strip(),
            password=hashed_pw,
            **kwargs
        )
        db.session.add(user)
        db.session.commit()
        return user

    def login_user(self, email, password):
        return self.model.query.filter_by(email=email.strip(), password=password.strip()).first()

