from flask import render_template, redirect, url_for, flash
from flask_login import login_user

from app.helpers.page_config_helper import get_page_config
from app.models import User
from app.helpers.forgot_password_form_helper import ForgotPasswordFormHelper
from app.helpers.login_form_helper import LoginFormHelper
from app.helpers.register_form_helper import RegisterFormHelper
from app.repositories import AuthRepository
from app.services import AuthService
from app.utils import auth

auth_service = AuthService(AuthRepository())

class AuthController:
    def register(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        form = RegisterFormHelper()
        if form.validate_on_submit():
            users = {
                "username": form.username.data,
                "email": form.email.data,
                "password": form.password.data,
                "confirm_password": form.confirm_password.data,
            }
            success, message = auth_service.register_user( **users)

            if success:
                flash(message, "success")
                return redirect(url_for('admin.login'))
            else:
                flash(message, "danger")
        return render_template(config['page_template'], **config, page_type=page_type, form=form)

    def login(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        form = LoginFormHelper()
        if form.validate_on_submit():
            user = {
                'email': form.email.data,
                'password': form.password.data,
            }
            user = auth_service.check_login( **user )
            if user:
                login_user(user)
                flash("Đăng nhập thành công", "success")
                return redirect(url_for('admin.dashboard'))
            else:
                flash("Tài khoản hoặc mật khẩu không đúng.", "danger")
        return render_template(config['page_template'], **config, page_type=page_type, form=form)

    def forgot_password(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        form = ForgotPasswordFormHelper()
        return render_template(config['page_template'], **config, page_type=page_type, form=form)