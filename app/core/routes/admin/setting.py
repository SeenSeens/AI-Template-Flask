from flask import render_template, request
from app.core.routes.admin import admin_bp
from app.core.controllers import SettingController
from flask_login import login_required
from app.core.routes.admin import admin_bp
from app.core.utils.decorators import admin_required
from app.core.config.page_config import PAGE_CONFIG

setting_controller = SettingController()
# Cài đặt

@admin_bp.route('/setting-general', methods=['GET', 'POST'])
@login_required
@admin_required
def general():
    page_type = request.args.get('page_type', 'setting')
    return setting_controller.general(page_type, 'general')

@admin_bp.route('/setting-writing', methods=['GET', 'POST'])
@login_required
@admin_required
def writing():
    page_type = request.args.get('page_type', 'setting')
    return setting_controller.general(page_type, 'writing')

@admin_bp.route('/setting-reading', methods=['GET', 'POST'])
@login_required
@admin_required
def reading():
    page_type = request.args.get('page_type', 'setting')
    return setting_controller.reading(page_type, 'reading')

@admin_bp.route('/setting-discussion', methods=['GET', 'POST'])
@login_required
@admin_required
def discussion():
    page_type = request.args.get('page_type', 'setting')
    return setting_controller.discussion(page_type, 'discussion')

@admin_bp.route('/setting-media', methods=['GET', 'POST'])
@login_required
@admin_required
def media():
    page_type = request.args.get('page_type', 'setting')
    return setting_controller.media(page_type, 'media')