from flask import render_template, abort, request, jsonify
from flask_login import login_required

from app.core.config.page_config import PAGE_CONFIG
from app.core.controllers import PostController

from app.core.routes.admin import admin_bp
from app.core.utils.decorators import admin_required

post_controller = PostController()
# @admin_bp.route('/post')
# def posts_redirect():
#     return post_controller.show_post('post')
# @admin_bp.route('/pages')
# def pages_redirect():
#     config = PAGE_CONFIG.get('pages')
#     if not config:
#         return "Không hợp lệ", 404
#     return render_template( config['page_template'], **config, page_type='pages' )

# Route hiển thị danh sách bài viết
@admin_bp.route('/post', methods=['GET', 'POST'])
@login_required
@admin_required
def posts():
    page_type = request.args.get('page_type')
    if page_type not in ['post', 'page']:
        abort(404)
    return post_controller.show_post(page_type, 'index')

# Route tạo bài viết mới
@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
@admin_required
def post_new():
    page_type = request.args.get('page_type')
    if page_type not in ['post', 'page']:
        abort(404)
    return post_controller.create_post(page_type, 'new')

# Route chỉnh sửa bài viết
@admin_bp.route('/post/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def post_edit():
    page_type = request.args.get('page_type')
    post_id = request.args.get('post_id', type=int)

    if page_type not in ['page', 'post'] or not post_id:
        abort(404)
    return post_controller.edit_post(page_type, 'edit', post_id)

@admin_bp.route('/post/delete', methods=['DELETE'])
@login_required
@admin_required
def post_delete():
    page_type = request.args.get('page_type')
    post_id = request.args.get('post_id', type=int)
    if page_type not in ['page', 'post'] or not post_id:
        abort(404)

    try:
        post_controller.delete_post(page_type, post_id)
        return jsonify({'success': True, 'message': 'Xoá thành công'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
