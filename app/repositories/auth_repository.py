import hashlib
from app import db
from app.models import User
class AuthRepository:
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

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
        return User.query.filter_by(email=email.strip(), password=password.strip()).first()

