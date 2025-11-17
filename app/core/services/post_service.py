from app.core.repositories import PostsRepository
class PostsService:
    def __init__(self, postRepository: PostsRepository):
        self.postRepository = postRepository

    # Lấy ra 1 bài viết theo id
    def get_post(self, post_id):
        return self.postRepository.get_post_by_id(post_id)

    # Lấy tất cả bài viết
    def get_posts(self, page_type):
        return self.postRepository.get_posts( page_type )

    # Tạo bài viết
    def create_post(self, **post_data):
        return self.postRepository.create_post( **post_data)
        # Xử lý thêm phần thêm bài viết vào chuyên mục

    # Cập nhật bài viết
    def update_post(self, post_id, **post_data):
        return self.postRepository.update_post( post_id, **post_data)

    # Xoá bài viết
    def delete_post(self, post_id):
        return self.postRepository.delete_post(post_id)