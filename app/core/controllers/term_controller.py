from flask import flash, redirect, url_for, render_template, jsonify

from app.core.config.page_config import PAGE_CONFIG
from app.core.helpers.page_config_helper import get_page_config
from app.core.helpers.term_form_helper import TermFormHelper
from app.core.services import TermService
from app.core.repositories import TermRepository
term_service = TermService(TermRepository())

class TermController:

    def show_terms(self, page_type, sub_type=None):
        config = get_page_config(page_type, sub_type)

        form = TermFormHelper()
        if form.validate_on_submit():
            name = form.name.data
            slug = form.slug.data
            description = form.description.data

            term_service.create_term_with_taxonomy(name, slug, description, page_type)
            flash('Tạo danh mục thành công', 'success')
            return redirect(url_for('admin.terms', page_type=page_type))

        terms = term_service.get_terms_by_taxonomy(page_type)

        return render_template(
            config['page_template'],
            config=config,
            page_type=page_type,
            **config,
            form=form,
            terms=terms,
            term=None
        )


    def edit_term(self, page_type, sub_type, term_id):
        config = get_page_config(page_type, sub_type)

        term = term_service.get(term_id)
        if not term:
            return "Không tìm thấy", 404

        form = TermFormHelper(obj=term)

        if form.validate_on_submit():

            term_data = {
                'name' : form.name.data,
                'slug' : form.slug.data,
                'description' : form.description.data
            }
            term_service.update(term_id, **term_data)
            flash('Cập nhật thành công', 'success')
            return redirect(url_for('admin.terms', page_type=page_type))

        terms = term_service.get_terms_by_taxonomy(page_type)
        return render_template(
            config['page_template'],
            config=config,
            page_type=page_type,
            **config,
            terms=terms,
            form=form,
            term=term
        )

    def delete_term(self, page_type, term_id):
        try:
            term_service.delete(term_id)
            flash("Đã xóa chuyên mục/thẻ!", "success")
        except Exception as e:
            flash(f"Lỗi khi xóa chuyên mục/thẻ: {str(e)}", "danger")
        return redirect(url_for('admin.terms', page_type=page_type))