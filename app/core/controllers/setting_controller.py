from app.core.helpers.page_config_helper import get_page_config
from flask import render_template
# from app.core.repositories import SettingRepository
# from app.core.services import SettingService

# setting_service = SettingService(SettingRepository())

class SettingController:

    def general(self, page_type, sub_type=None):
        config = get_page_config(page_type, sub_type)
        return render_template(config['page_template'], **config, page_type=page_type)

    def writing(self, page_type, sub_type=None):
        config = get_page_config(page_type, sub_type)
        return render_template(config['page_template'], **config, page_type=page_type)

    def reading(self, page_type, sub_type=None):
        config = get_page_config(page_type, sub_type)
        return render_template(config['page_template'], **config, page_type=page_type)

    def discussion(self, page_type, sub_type=None):
        config = get_page_config(page_type, sub_type)
        return render_template(config['page_template'], **config, page_type=page_type)

    def media(self, page_type, sub_type=None):
        config = get_page_config(page_type, sub_type)
        return render_template(config['page_template'], **config, page_type=page_type)

