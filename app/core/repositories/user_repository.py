from app.core import db
from .base_repository import BaseRepository
from app.core.models import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def is_duplicate(self, user_id, username, email):
        query = self.model.query.filter(
            ((self.model.username == username) | (self.model.email == email)),
            self.model.id != user_id
        )
        return db.session.query(query.exists()).scalar()