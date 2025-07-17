from app.repositories.ai_preset_repository import AIPresetRepository


class AIPresetService:
    def __init__(self, repository: AIPresetRepository):
        self.repository = repository

    def create_ai_preset(self, **kwargs):
        return self.repository.create_ai_preset(**kwargs)

    def get_all_ai_presets(self):
        return self.repository.get_all_ai_presets()