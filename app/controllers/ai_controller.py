from flask import render_template, request, jsonify
from app.helpers.ai_configuration_helper import AIConfigurationHelper
from app.helpers.page_config_helper import get_page_config
from app.repositories import AiConfigRepository
from app.services.ai_config_service import AiConfigService

service = AiConfigService(AiConfigRepository())

class AIController:

    def load_models(self, provider, api_key, task=None):

        try:
            print("📥 Controller nhận:", provider, api_key[:10], "...", task)

            if provider.lower() == 'huggingface':
                models = service._get_huggingface_models(api_key, task=task)
            else:
                models = service.fetch_models(api_key, provider)

            if isinstance(models[0], str):
                formatted = [{"id": m, "label": m} for m in models]
            else:
                formatted = [{"id": m["id"], "label": f'{m["id"]} ❤️ {m.get("likes", 0)}'} for m in models]

            return jsonify({"models": formatted})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": f"Lỗi controller: {str(e)}"}), 400

    def ai_configuration(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        form = AIConfigurationHelper()
        return render_template(config['page_template'], **config, form=form, page_type=page_type)