from app.core import  db
from app.core.models.posts import Post
from .base_repository import BaseRepository

class PostsRepository(BaseRepository):

    def __init__(self):
        super().__init__(Post)

    def get_posts_by_type(self, page_type):
        return self.get_all(type=page_type)