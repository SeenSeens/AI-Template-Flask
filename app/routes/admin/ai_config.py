from flask import request, jsonify, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.controllers import AIController
from app.helpers.ai_configuration_helper import AIConfigurationHelper
from app.repositories import AiConfigRepository
from app.routes.admin import admin_bp
from app.services import AiConfigService
from app.utils.decorators import admin_required

ai_controller = AIController()
service = AiConfigService(AiConfigRepository())

# Load Model AI
@admin_bp.route('/load-models', methods=['POST'])
@login_required
@admin_required
def load_models():
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
@admin_bp.route('/ai-configuration', methods=['GET', 'POST'])
@login_required
@admin_required
def ai_configuration():
    return ai_controller.ai_configuration('ai', 'configuration')

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

