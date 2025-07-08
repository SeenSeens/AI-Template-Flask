from app.repositories import AIPresetFeatureRepository


class AIPresetFeatureService:
    def __init__(self, repository: AIPresetFeatureRepository):
        self.repository = repository

    def create_ai_preset_feature(self, **kwargs):
        return self.repository.create_ai_preset_feature(**kwargs)