import hashlib

from app.core.repositories import UserRepository


class UserService:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    # Lấy ra 1 user theo id
    def get_user(self, user_id):
        return self.userRepository.get_user_by_id(user_id)

    # Lấy tất cả user
    def get_users(self):
        return self.userRepository.get_users()

    # Thêm mới uer
    def create_user(self, **user_data):
        password_plain = user_data.get('password')
        if password_plain:
            hashed_password = hashlib.md5(password_plain.encode('utf-8')).hexdigest()
            user_data['password'] = hashed_password
        return self.userRepository.create_user(**user_data)

    # Cập nhật user
    def update_user(self, user_id, **user_data):
        if 'password' in user_data:
            user_data['password'] = hashlib.md5(user_data['password'].encode('utf-8')).hexdigest()

        # Kiểm tra unique email/username nếu thay đổi
        if self.userRepository.is_duplicate(user_id, user_data.get('username'), user_data.get('email')):
            raise Exception("Username hoặc email đã tồn tại.")
        return self.userRepository.update_user(user_id, **user_data)

    # Xoá user
    def delete_user(self, user_id):
        return self.userRepository.delete_user(user_id)