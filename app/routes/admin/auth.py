from flask import render_template, redirect, url_for
from flask_login import logout_user

from app.controllers import AuthController
from app.helpers.forgot_password_form_helper import ForgotPasswordFormHelper
from app.helpers.login_form_helper import LoginFormHelper
from app.helpers.register_form_helper import RegisterFormHelper
from app.routes.admin import admin_bp

auth_controller = AuthController()
@admin_bp.route('/')
def admin_redirect():
    return redirect(url_for('admin.login'))

@admin_bp.route('/register', methods = [ 'GET', 'POST'])
def register() :
    return auth_controller.register()

@admin_bp.route('/login', methods = [ 'GET', 'POST'])
def login() :
    return auth_controller.login()

@admin_bp.route('/forgot-password', methods = [ 'GET', 'POST'])
def forgot_password() :
    return auth_controller.forgot_password()

@admin_bp.route('/logout')
def logout() :
    logout_user()
    return redirect(url_for('admin.login'))