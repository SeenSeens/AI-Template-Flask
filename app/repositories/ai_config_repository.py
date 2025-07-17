from app import db, AIConfig


class AIConfigRepository:
    def get_ai_config_id(self, id_ai_config):
        return AIConfig.query.get_or_404(id_ai_config)

    def get_config_by_user(self, user_id):
        return AIConfig.query.filter_by(user_id=user_id).first()

    def get_config_by_user_and_provider(self, user_id, provider):
        return AIConfig.query.filter_by(user_id=user_id, provider=provider).first()

    def save_or_update_config(self, user_id, data):
        config = self.get_config_by_user(user_id)
        if config:
            for key, value in data.items():
                setattr(config, key, value)
        else:
            config = AIConfig(user_id=user_id, **data)
            db.session.add(config)
        db.session.commit()
        return config

    def create_ai_config(self, **ai_config_data):
        ai_configs = AIConfig(**ai_config_data)
        db.session.add(ai_configs)
        db.session.commit()
        return ai_configs

    def update_ai_config(self, id_config, **ai_config_data):
        ai_config = self.get_ai_config_id(id_config)
        try:
            for key, value in ai_config_data.items():
                setattr(ai_config, key, value)  # Gán từng field
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def get_all_configs(self):
        return AIConfig.query.all()

    def delete_ai_config(self, id_config):
        ai_config = AIConfig.query.get_or_404(id_config)
        try:
            db.session.delete(ai_config)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e