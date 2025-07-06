from flask import request, jsonify, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.controllers import AIConfigController
from app.helpers.ai_configuration_helper import AIConfigurationHelper
from app.repositories import AiConfigRepository
from app.routes.admin import admin_bp
from app.services import AiConfigService
from app.utils.decorators import admin_required

ai_config_controller = AIConfigController()
service = AiConfigService(AiConfigRepository())

# Load Model AI
@admin_bp.route('/load-models', methods=['POST'])
@login_required
@admin_required
def load_models():
    return ai_config_controller.load_models()

# Kiểm tra kết nối
@login_required
@admin_required
@admin_bp.route('/test-connection', methods=['POST'])
def test_connection():
    return ai_config_controller.test_connection()

# Cấu hình AI
@admin_bp.route('/ai-configuration', methods=['GET', 'POST'])
@login_required
@admin_required
def ai_configuration():
    return ai_config_controller.ai_configuration('ai', 'configuration')


# Lấy ra tất cả model ai
@admin_bp.route('/ai-all')
@login_required
@admin_required
def all_ai():
    return ai_config_controller.all_ai('ai', 'all_ai')


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
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Cấu hình Ai sinh nội dung
@admin_bp.route('/config-content-ai', methods=['GET', 'POST'])
@login_required
@admin_required
def config_content_ai():
    return ai_config_controller.config_content_ai('ai', 'content_ai')

# Sinh giao diện
@admin_bp.route('/config-design-ai')
@login_required
@admin_required
def config_design_ai():
    return ai_config_controller.config_design_ai('ai', 'design_ai')

# Xử lý ảnh AI
@admin_bp.route('/config-image-processing-ai')
@login_required
@admin_required
def config_image_processing_ai():
    return ai_config_controller.config_image_processing_ai('ai', 'image_processing_ai')
