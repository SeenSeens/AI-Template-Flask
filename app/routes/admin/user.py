from flask import render_template, request, abort, jsonify
from flask_login import login_required, current_user

from app.config.page_config import PAGE_CONFIG
from app.controllers import UserController
from app.routes.admin import admin_bp
from app.utils.decorators import admin_required

user_controller = UserController()

@admin_bp.route('/user')
@login_required
@admin_required
def users():
    return user_controller.show_users('user', 'index')

@admin_bp.route('/user/new', methods=['GET', 'POST'])
@login_required
@admin_required
def user_new():
    return user_controller.create_user('user', 'new')

@admin_bp.route('/user/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit():
    user_id = request.args.get('user_id', type=int)
    return user_controller.edit_user('user', 'edit', user_id)

@admin_bp.route('/user/profile', methods=['GET', 'POST'])
def profile():
    user_id = request.args.get('user_id', type=int)
    return user_controller.user_profile('user', 'profile', user_id)

@admin_bp.route('/user/delete', methods=['DELETE'])
@login_required
@admin_required
def user_delete():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'success': False, 'message': 'Tham số không hợp lệ'}), 400

    try:
        user_controller.delete_user(user_id)
        return jsonify({'success': True, 'message': 'Xoá thành công'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

