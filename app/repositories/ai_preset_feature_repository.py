from app import AIPresetFeature, db


class AIPresetFeatureRepository:
    def create_ai_preset_feature(self, **ai_preset_feature_data):
        ai_preset_feature = AIPresetFeature(**ai_preset_feature_data)
        db.session.add(ai_preset_feature)
        db.session.commit()
        return ai_preset_feature