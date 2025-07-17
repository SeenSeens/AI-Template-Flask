from flask_login import login_required

from app.routes.admin import admin_bp
from app.controllers.ai_preset_controller import AIPresetController
from app.utils.decorators import admin_required

ai_preset_controller = AIPresetController()

@admin_bp.route('/config-content-ai', methods=['GET', 'POST'])
@login_required
@admin_required
def config_content_ai():
    return ai_preset_controller.config_content_ai('ai', 'content_ai')

