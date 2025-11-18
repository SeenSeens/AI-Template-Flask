import hashlib
from .base_service import BaseService
from app.core.repositories import UserRepository


class UserService(BaseService):
    def __init__(self, userRepository: UserRepository):
        super().__init__(userRepository)

    def create_user(self, **user_data):
        password_plain = user_data.get('password')
        if password_plain:
            user_data['password'] = hashlib.md5(password_plain.encode('utf-8')).hexdigest()
        return self.repository.create(**user_data)

    def update_user(self, user_id, **user_data):
        if 'password' in user_data:
            user_data['password'] = hashlib.md5(user_data['password'].encode('utf-8')).hexdigest()

        if self.repository.is_duplicate(user_id, user_data.get('username'), user_data.get('email')):
            raise Exception("Username hoặc email đã tồn tại.")

        return self.repository.update(user_id, **user_data)