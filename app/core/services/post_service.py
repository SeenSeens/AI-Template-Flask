from app.core.repositories import PostsRepository
from .base_service import BaseService

class PostsService(BaseService):
    def __init__(self, postRepository: PostsRepository):
        super().__init__(postRepository)

    def get_posts(self, page_type):
        return self.repository.get_posts_by_type(page_type)
