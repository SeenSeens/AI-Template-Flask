from flask import request, abort, jsonify
from flask_login import login_required
from app.utils.decorators import admin_required
from app.controllers import TermController
from app.routes.admin import admin_bp

term_controller = TermController()
@admin_bp.route('/term', methods=['GET', 'POST'])
@login_required
@admin_required
def terms():
    page_type = request.args.get('page_type')
    if page_type not in ['category', 'tag']:
        abort(404)
    return term_controller.show_terms(page_type)

@admin_bp.route('/term/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def term_edit():
    page_type = request.args.get('page_type')
    term_id = request.args.get('term_id', type=int)

    if page_type not in ['category', 'tag'] or not term_id:
        abort(404)
    return term_controller.edit_term(page_type, 'edit', term_id)

@admin_bp.route('/term/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_term():
    page_type = request.args.get('page_type')
    term_id = request.args.get('term_id', type=int)
    if page_type not in ['category', 'tag'] or not term_id:
        abort(404)

    try:
        term_controller.delete_term(page_type, term_id)
        return jsonify({'success': True, 'message': 'Xoá thành công'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400