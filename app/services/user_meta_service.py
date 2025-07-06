from app.repositories import UserMetaRepository

class UserMetaService:
    def __init__(self, userMetaRepository: UserMetaRepository):
        self.userMetaRepository = userMetaRepository

    def get_meta(self, user_id, key):
        meta = self.userMetaRepository.get_by_user_and_key(user_id, key)
        return meta.meta_value if meta else None

    def get_all(self, user_id):
        return self.userMetaRepository.get_all_by_user(user_id)

    def set_meta(self, user_id, key, value):
        return self.userMetaRepository.set_meta(user_id, key, value)

    def delete_meta(self, user_id, key):
        return self.userMetaRepository.delete_meta(user_id, key)
