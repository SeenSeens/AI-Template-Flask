from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.helpers.page_config_helper import get_page_config
from app.helpers.post_form_helper import PostFormHelper
from app.helpers.post_term_relationships_helper import PostTermRelationshipsHelper
from app.repositories import PostsRepository, TermRepository
from app.services import PostsService, TermService

post_service = PostsService(PostsRepository())
term_service = TermService(TermRepository())

class PostController:

    def show_post(self, page_type, sub_type=None):

        config = get_page_config(page_type, sub_type)
        posts = post_service.get_posts(page_type)
        return render_template(config['page_template'], **config, page_type=page_type, posts=posts)

    def create_post(self, page_type, sub_type=None):

        config = get_page_config(page_type, sub_type)

        form = PostFormHelper()
        categories = term_service.get_terms_by_taxonomy('category')
        tags = term_service.get_terms_by_taxonomy('tag')
        form_term = PostTermRelationshipsHelper()
        form_term.category.choices = [(category.id, category.name) for category in categories]
        form_term.tag.choices = [(tag.id, tag.name) for tag in tags]

        if form.validate_on_submit():
            status = 'draft' if form.submit_draft.data else 'publish'
            post_data = {
                'title': form.title.data,
                'slug': form.slug.data,
                'content': form.content.data,
                'excerpt': form.excerpt.data,
                'status': status,
                'type': page_type,
                'author_id': current_user.id,
            }
            try:
                post_service.create_post( **post_data)
                if status == 'draft':
                    flash("Lưu nháp thành công!", "info")
                else:
                    flash("Tạo bài viết thành công!", "success")
            except Exception as e:
                flash(f"Lỗi khi tạo bài viết: {str(e)}", "danger")
        return render_template( config['page_template'], **config, page_type=page_type, form=form, form_term=form_term)

    def edit_post(self, page_type, sub_type, post_id):
        config = get_page_config(page_type, sub_type)

        post = post_service.get_post( post_id)

        if not post:
            flash("Không tìm thấy bài viết!", "danger")
            return redirect(url_for('admin.posts', page_type=page_type))

        form = PostFormHelper(obj=post)

        categories = term_service.get_terms_by_taxonomy('category')
        tags = term_service.get_terms_by_taxonomy('tag')
        form_term = PostTermRelationshipsHelper()
        form_term.category.choices = [(category.id, category.name) for category in categories]
        form_term.tag.choices = [(tag.id, tag.name) for tag in tags]

        if form.validate_on_submit():
            status = 'draft' if form.submit_draft.data else 'publish'
            post_data = {
                'title': form.title.data,
                'slug': form.slug.data,
                'content': form.content.data,
                'excerpt': form.excerpt.data,
                'status': status,
                'type': page_type,
                'author_id': current_user.id,
            }
            try:
                post_service.update_post(post_id, **post_data)
                if status == 'draft':
                    flash("Lưu nháp thành công!", "info")
                else:
                    flash("Cập nhật bài viết thành công!", "success")
            except Exception as e:
                flash(f"Lỗi khi tạo bài viết: {str(e)}", "danger")

        return render_template(
            config['page_template'],
            **config,
            page_type=page_type,
            post=post,
            form=form,
            form_term=form_term
        )

    def delete_post(self, page_type, post_id):
        try:
            post_service.delete_post(post_id)
            flash("Đã xóa bài viết!", "success")
        except Exception as e:
            flash(f"Lỗi khi xóa bài viết: {str(e)}", "danger")
        return redirect(url_for('admin.posts', page_type=page_type))