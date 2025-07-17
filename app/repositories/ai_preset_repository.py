from app import AIPreset, db


class AIPresetRepository:
    def create_ai_preset(self, **ai_preset_data):
        ai_preset = AIPreset(**ai_preset_data)
        db.session.add(ai_preset)
        db.session.commit()
        return ai_preset

    def get_all_ai_presets(self):
        return AIPreset.query.all()