from app import db
from app.models import User

class UserRepository:
    # Lấy ra 1 user theo id
    def get_user_by_id(self, user_id):
        return User.query.get_or_404(user_id)

    def is_duplicate(self, user_id, username, email):
        query = User.query.filter(
            ((User.username == username) | (User.email == email)),
            User.id != user_id
        )
        return db.session.query(query.exists()).scalar()

    # Lấy ra tất cả user
    def get_users(self):
        return User.query.all()

    # Thêm mới user
    def create_user(self, **user_data):
        existing = User.query.filter(
            (User.username == user_data['username']) |
            (User.email == user_data['email'])
        ).first()
        if existing:
            raise Exception("Username hoặc email đã tồn tại.")
        user = User(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e

    def update_user(self, user_id, **user_data):
        user = self.get_user_by_id(user_id)
        try:
            for key, value in user_data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e