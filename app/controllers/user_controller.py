from flask import render_template, flash, redirect, url_for, request

from app import db
from app.helpers.page_config_helper import get_page_config
from app.helpers.user_form_helper import UserFormHelper
from app.helpers.user_meta_form_helper import UserMetaFormHelper
from app.repositories import UserRepository, UserMetaRepository
from app.services import UserService, UserMetaService

user_service = UserService(UserRepository())
user_meta_service = UserMetaService(UserMetaRepository())

class UserController:
    def show_users(self, page_type, sub_type=None):
        config = get_page_config(page_type, sub_type)
        users = user_service.get_users()
        return render_template(config['page_template'], **config, users=users)

    def user_profile(self, page_type, sub_type=None, user_id=None):
        config = get_page_config(page_type, sub_type)
        user = user_service.get_user(user_id)
        form = UserMetaFormHelper(obj=user)

        # Load thêm từ user_meta (nếu có phone, mobile, address trong đó)
        for field in ['phone', 'mobile', 'address']:
            if hasattr(form, field):
                meta_value = user_meta_service.get_meta(user_id, field)
                getattr(form, field).data = meta_value

        # Xử lý POST submit form
        if form.validate_on_submit():
            # Cập nhật User
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit()

            # Cập nhật Meta
            for field in ['phone', 'mobile', 'address']:
                user_meta_service.set_meta(user.id, field, getattr(form, field).data)

            flash('Cập nhật thông tin người dùng thành công!', 'success')
            return redirect(url_for('admin.profile', user_id=user.id))
        return render_template(config['page_template'], **config, user=user, form=form)

    def create_user(self, page_type, sub_type=None):
        config = get_page_config(page_type, sub_type)
        form = UserFormHelper()
        if form.validate_on_submit():
            user_data = {
                'username': form.username.data,
                'email': form.email.data,
                'password': form.password.data,
                'role': form.role.data,
                'status': form.status.data,
            }
            try:
                user_service.create_user( **user_data)
                flash('Người dùng đã được thêm thành công!', 'success')
            except Exception as e:
                flash(f"Lỗi khi tạo người dùng: {str(e)}", "danger")
            return redirect(url_for('admin.users'))
        return render_template(config['page_template'], **config, form=form)

    def edit_user(self, page_type, sub_type, user_id):
        config = get_page_config(page_type, sub_type)
        user = user_service.get_user(user_id)
        if not user:
            flash("Người dùng không tồn tại!", "danger")
            return redirect(url_for('admin.users'))
        form = UserFormHelper(obj=user)
        if form.validate_on_submit():
            user_data = {
                'username': form.username.data,
                'email': form.email.data,
                'role': form.role.data,
                'status': form.status.data,
            }
            # Chỉ cập nhật nếu người dùng nhập mật khẩu mới
            if form.password.data.strip():
                user_data['password'] = form.password.data
            try:
                user_service.update_user(user_id, **user_data)
                flash('Cập nhật người dùng thành công!', 'success')
            except Exception as e:
                flash(f"Lỗi khi cập nhật người dùng: {str(e)}", "danger")
            return redirect(url_for('admin.users'))
        return render_template(
            config['page_template'],
            **config,
            form=form,
            user=user
        )

    def delete_user(self, user_id):
        try:
            user_service.delete_user(user_id)
            flash("Đã xóa người dùng!", "success")
        except Exception as e:
            flash(f"Lỗi khi xóa người dùng: {str(e)}", "danger")
        return redirect(url_for('admin.users'))