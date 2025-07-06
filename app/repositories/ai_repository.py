from app import AiConfigs, db
class AiRepository:
    def get_config_by_user(self, user_id):
        return AiConfigs.query.filter_by(user_id=user_id).first()

    def get_config_by_user_and_provider(self, user_id, provider):
        return AiConfigs.query.filter_by(user_id=user_id, provider=provider).first()

    def save_or_update_config(self, user_id, data):
        config = self.get_config_by_user(user_id)
        if config:
            for key, value in data.items():
                setattr(config, key, value)
        else:
            config = AiConfigs(user_id=user_id, **data)
            db.session.add(config)
        db.session.commit()
        return config

    def create_ai_config(self, **ai_config_data):
        ai_configs = AiConfigs(**ai_config_data)
        db.session.add(ai_configs)
        db.session.commit()
        return ai_configs

    def get_all_configs(self):
        return AiConfigs.query.all()
