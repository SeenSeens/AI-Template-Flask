from app.core.repositories import SettingRepository

class SettingService:
    def __init__(self, settingRepository: SettingRepository):
        self.settingRepository = settingRepository