from app.core import db

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, obj_id):
        return self.model.query.get_or_404(obj_id)

    def get_all(self, **filters):
        return self.model.query.filter_by(**filters).all()

    def create(self, **data):
        obj = self.model(**data)
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, obj_id, **data):
        obj = self.get_by_id(obj_id)
        try:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self, obj_id):
        obj = self.get_by_id(obj_id)
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def filter(self, **filters):
        return self.model.query.filter_by(**filters)
