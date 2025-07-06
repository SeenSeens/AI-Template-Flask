from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user
from app.helpers.ai_configuration_helper import AIConfigurationHelper
from app.helpers.page_config_helper import get_page_config
from app.repositories import AiConfigRepository
from app.services.ai_config_service import AiConfigService

service = AiConfigService(AiConfigRepository())

class AIConfigController:

    def load_models(self):
        if not request.is_json:
            return jsonify({'error': 'Content-Type phải là application/json'}), 400

        data = request.get_json()
        provider = data.get("provider")
        api_key = data.get("token")
        task = data.get("task")

        if not api_key or not provider:
            return jsonify({'error': 'Missing API key or provider'}), 400

        try:
            if provider.lower() == 'huggingface':
                models = service._get_huggingface_models(api_key, task=task)
            else:
                models = service.fetch_models(api_key, provider)

            if isinstance(models[0], str):
                formatted_models = [{"id": m, "label": m} for m in models]
            else:
                formatted_models = [
                    {"id": m["id"], "label": f'{m["id"]} ❤️ {m.get("likes", 0)}'}
                    for m in models
                ]

            return jsonify({"models": formatted_models})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def test_connection(self):
        data = request.get_json()
        api_key = data.get('api_key')
        provider = data.get('provider')
        if not api_key or not provider:
            return jsonify({'error': 'Thiếu API key hoặc provider'}), 400
        try:
            service.fetch_models(api_key, provider)  # đơn giản chỉ cần fetch được models
            return jsonify({'message': 'Kết nối thành công với nhà cung cấp AI.'})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    def ai_configuration(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        form = AIConfigurationHelper()
        if form.token.data and form.provider.data == 'huggingface':
            try:
                models = service.fetch_models(form.token.data, 'huggingface')
                form.model_name.choices = [('', '-- Chọn model --')] + [
                    (
                        m["id"],  # value
                        f'{m["id"]} ❤️ {m.get("likes", 0)}'  # label
                    )
                    for m in models
                ]
            except Exception as e:
                flash(f"Lỗi khi tải model Hugging Face: {str(e)}", "danger")

        if form.validate_on_submit():
            # Gom toàn bộ thông tin vào dict để dễ xử lý
            ai_config_data = {
                'provider': form.provider.data,
                'user_id': current_user.id,
                'model_name': form.model_name.data,
                'api_key': form.token.data,
            }
            service.create_ai_config(**ai_config_data)
            flash('AI configuration saved successfully.', 'success')
            return redirect(url_for('admin.ai_configuration'))
        return render_template(config['page_template'], **config, form=form, page_type=page_type)

    def all_ai(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        all_ai = service.get_all_configs()
        return render_template(config['page_template'], **config, page_type=page_type, all_ai=all_ai)

    def config_content_ai(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        if request.method == 'POST':
            data = request.get_json()
            prompt = data.get('prompt')
            if not prompt:
                return jsonify({'error': 'Vui lòng nhập yêu cầu nội dung'}), 400

            try:
                # Gọi service sinh content với Gemini
                content = service.generate_content_with_gemini(prompt, current_user.id)
                return jsonify({'content': content})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        return render_template(config['page_template'], **config, page_type=page_type)

    def config_design_ai(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        return render_template(config['page_template'], **config, page_type=page_type)

    def config_image_processing_ai(self, page_type, sub_type):
        config = get_page_config(page_type, sub_type)
        return render_template(config['page_template'], **config, page_type=page_type)