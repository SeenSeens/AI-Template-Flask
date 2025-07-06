from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from app.models import User
from app.helpers.forgot_password_form_helper import ForgotPasswordFormHelper
from app.helpers.login_form_helper import LoginFormHelper
from app.helpers.register_form_helper import RegisterFormHelper
from app.repositories import AuthRepository
from app.services import AuthService
from app.utils import auth

auth_service = AuthService(AuthRepository())

class AuthController:
    def register(self):
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
        return render_template('admin/pages/auth/register.html', form=form)

    def login(self):
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
                flash("Incorrect account or password.", "danger")
        return render_template('admin/pages/auth/login.html', form=form)

    def forgot_password(self):
        form = ForgotPasswordFormHelper()
        return render_template('admin/pages/auth/forgot-password.html', form=form)