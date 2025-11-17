from app.core import  db
from app.core.models.posts import Post

class PostsRepository:

    # Lấy ra 1 bài viết theo id
    def get_post_by_id(self, post_id):
        return Post.query.get_or_404(post_id)
    # Lấy ra tất cả bài viết
    def get_posts(self, page_type):
        return Post.query.filter_by(type=page_type).all()
    # Thêm bài viết mới
    def create_post(self, **post_data):
        post = Post( **post_data)
        try:
            db.session.add(post)
            db.session.commit()
            return post
        except Exception as e:
            db.session.rollback()
            raise e

    def update_post(self, post_id, **post_data):
        post = Post.query.get_or_404(post_id)
        try:
            for key, value in post_data.items():
                setattr(post, key, value)
            db.session.commit()
            return post
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_post(self, post_id):
        post = Post.query.get_or_404(post_id)
        try:
            db.session.delete(post)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e