from app.core import db
from app.core.models import UserMeta

class UserMetaRepository:
    def get_by_user_and_key(self, user_id, key):
        return UserMeta.query.filter_by(user_id=user_id, meta_key=key).first()

    def get_all_by_user(self, user_id):
        return UserMeta.query.filter_by(user_id=user_id).all()

    def set_meta(self, user_id, key, value):
        safe_value = value if value is not None else ''
        meta = self.get_by_user_and_key(user_id, key)
        if meta:
            meta.meta_value = safe_value
        else:
            meta = UserMeta(user_id=user_id, meta_key=key, meta_value=safe_value)
            db.session.add(meta)

        try:
            db.session.commit()
            return meta
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_meta(self, user_id, key):
        meta = self.get_by_user_and_key(user_id, key)
        if meta:
            try:
                db.session.delete(meta)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
