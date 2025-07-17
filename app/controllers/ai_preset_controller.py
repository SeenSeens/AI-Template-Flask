from flask import flash, render_template
from app.helpers.ai_preset_form_helper import AIPresetFormHelper
from app.helpers.page_config_helper import get_page_config
from app.repositories import AIPresetFeatureRepository
from app.repositories.ai_preset_repository import AIPresetRepository
from app.services.ai_preset_feature_service import AIPresetFeatureService
from app.services.ai_preset_service import AIPresetService

servicePreset = AIPresetService(AIPresetRepository())
servicePresetFeature = AIPresetFeatureService(AIPresetFeatureRepository())

class AIPresetController:
    def config_content_ai(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        form = AIPresetFormHelper()
        if form.validate_on_submit():
            ai_preset_data = {
                'use_case': form.use_case.data,
                'type': form.type.data,
                'temperature': form.temperature.data,
                'top_p': form.top_p.data,
                'max_tokens': form.max_tokens.data,
                'frequency_penalty': form.frequency_penalty.data,
            }
            preset = servicePreset.create_ai_preset(**ai_preset_data)
            ai_preset_feature_data = {
                'preset_id': preset.id,
                'is_default': form.is_default.data,
                'autocomplete': form.autocomplete.data,
                'summarize': form.summarize.data,
                'translate': form.translate.data,
                'multi_chat': form.multi_chat.data,
                'features': form.features.data if hasattr(form, 'features') else [],
            }

            servicePresetFeature.create_ai_preset_feature(**ai_preset_feature_data)
            flash('Cấu hình AI đã được lưu thành công.', 'success')
            # return redirect(url_for('admin.ai_configuration'))
        presets = servicePreset.get_all_ai_presets()
        return render_template(config['page_template'], **config, page_type=page_type, form=form, presets=presets)