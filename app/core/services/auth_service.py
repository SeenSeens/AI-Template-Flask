import hashlib
from flask_login import login_user
from app.core.models import User
from app.core.repositories import AuthRepository
from .base_service import BaseService

class AuthService(BaseService) :
    def __init__(self, authRepository: AuthRepository):
        super().__init__(authRepository)

    def hash_password(self, password):
        return str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    def register_user(self, username, email, password, confirm_password):
        if self.repository.get_by_username(username):
            return False, "Tên người dùng đã có người sử dụng!"

        if password.strip() != confirm_password.strip():
            return False, "Mật khẩu không khớp"

        try:
            self.repository.register_user(username, email, password)
            return True, "Đăng ký thành công"
        except Exception as e:
            return False, f"Hệ thống đang có lỗi: {str(e)}"

    def check_login(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        if not email or not password:
            return None
        hashed_password = self.hash_password(password)
        return self.repository.login_user(email, hashed_password)