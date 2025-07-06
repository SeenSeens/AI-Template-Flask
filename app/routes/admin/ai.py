from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from app.helpers.ai_configuration_helper import AIConfigurationHelper
from app.repositories.ai_repository import AiRepository
from app.routes.admin import admin_bp
from app.services import AiService

from app.utils.decorators import admin_required
service = AiService(AiRepository())


# Load Model AI
@login_required
@admin_required
@admin_bp.route('/load-models', methods=['GET', 'POST'])
def load_models():
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
            # Trường hợp OpenAI, Anthropic, Gemini
            formatted_models = [{"id": m, "label": m} for m in models]
        else:
            # Trường hợp HuggingFace trả về object
            formatted_models = [
                {
                    "id": m["id"],
                    "label": f'{m["id"]} ❤️ {m.get("likes", 0)}'
                }
                for m in models
            ]

        return jsonify({"models": formatted_models})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Kiểm tra kết nối
@login_required
@admin_required
@admin_bp.route('/test-connection', methods=['POST'])
def test_connection():
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

# Cấu hình AI
@login_required
@admin_required
@admin_bp.route('/ai-configuration', methods=['GET', 'POST'])
def ai_configuration():
    form_helper = AIConfigurationHelper()
    # if request.method == 'POST':
    #     form = request.form
    #
    #     data = {
    #         'provider': form.get('provider'),
    #         'model_name': form.get('model_name'),
    #         'api_key': form.get('token'),
    #         'temperature': float(form.get('temperature', 0.7)),
    #         'top_p': float(form.get('top_p', 1.0)),
    #         'max_tokens': int(form.get('max_tokens', 512)),
    #         'frequency_penalty': float(form.get('frequency_penalty', 0.0)),
    #         'autocomplete': 'autocomplete' in form,
    #         'summarize': 'summarize' in form,
    #         'translate': 'translate' in form,
    #         'multi_chat': 'multi_chat' in form,
    #         'features': {},  # bạn có thể thêm logic thêm features nếu có field ẩn
    #     }
    #
    #     success, message = service.validate_and_save_config(data, current_user.id)
    #     flash(message, 'success' if success else 'danger')
    #     return redirect(url_for('admin.ai_configuration'))

    # Nếu GET, lấy config hiện tại để đổ vào form
    config = service.get_user_config(current_user.id)
    if form_helper.token.data and form_helper.provider.data == 'huggingface':
        try:
            models = service.fetch_models(form_helper.token.data, 'huggingface')
            form_helper.model_name.choices = [('', '-- Chọn model --')] + [
                (
                    m["id"],  # value
                    f'{m["id"]} ❤️ {m.get("likes", 0)}'  # label
                )
                for m in models
            ]
        except Exception as e:
            flash(f"Lỗi khi tải model Hugging Face: {str(e)}", "danger")

    # print(form_helper.errors)

    if form_helper.validate_on_submit():
        # Gom toàn bộ thông tin vào dict để dễ xử lý
        ai_config_data = {
            'provider': form_helper.provider.data,
            'user_id': current_user.id,
            'model_name': form_helper.model_name.data,
            'api_key': form_helper.token.data,
            'temperature': form_helper.temperature.data,
            'top_p': form_helper.top_p.data,
            'max_tokens': form_helper.max_tokens.data,
            'frequency_penalty': form_helper.frequency_penalty.data,
            'features': form_helper.features.data if hasattr(form_helper, 'features') else [],
            'autocomplete': form_helper.autocomplete.data,
            'summarize': form_helper.summarize.data,
            'translate': form_helper.translate.data,
            'multi_chat': form_helper.multi_chat.data,
        }
        service.create_ai_config(**ai_config_data)
        flash('AI configuration saved successfully.', 'success')
        return redirect(url_for('admin.ai_configuration'))
    return render_template('admin/pages/ai/ai_configuration.html', form_helper=form_helper, config=config)

# Lấy ra tất cả model ai
@admin_bp.route('/ai-configs/all')
@login_required
@admin_required
def all_ai_configs():

    configs = service.get_all_configs()
    return render_template('admin/pages/ai/all_ai_configs.html', configs=configs)

@admin_bp.route("/generate-ai-post", methods=["POST"])
@login_required
@admin_required
def generate_ai_post():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Thiếu prompt"}), 400

    try:
        content = service.generate_content_with_gemini(prompt=prompt, user_id=current_user.id)
        return jsonify( content )
    except Exception as e:
        return jsonify({"error": str(e)}), 400




# Sinh nội dung
@admin_bp.route('/generate-content', methods=['GET', 'POST'])
# @login_required
# @admin_required
def generate_content():
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
    return render_template('admin/pages/ai/generate_content.html')

# Sinh giao diện
@admin_bp.route('/generate-interface')
# @login_required
# @admin_required
def generate_interface():
    return render_template('admin/pages/ai/generate_interface.html')

# Xử lý ảnh AI
@admin_bp.route('/ai-image-processing')
# @login_required
# @admin_required
def ai_image_processing():
    return render_template('admin/pages/ai/ai_image_processing.html')
