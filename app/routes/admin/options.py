from flask import render_template
from app.config.page_config import PAGE_CONFIG
from app.routes.admin import admin_bp

# Cài đặt

@admin_bp.route('/<string:page_type>')
def overview(page_type):
    config = PAGE_CONFIG.get(page_type)
    if not config:
        return "Không hợp lệ", 404
    return render_template( config['page_template'], **config, page_type=page_type )

@admin_bp.route('/<string:page_type>')
def write(page_type):
    config = PAGE_CONFIG.get(page_type)
    if not config:
        return "Không hợp lệ", 404
    return render_template( config['page_template'], **config, page_type=page_type )

@admin_bp.route('/<string:page_type>')
def read(page_type):
    config = PAGE_CONFIG.get(page_type)
    if not config:
        return "Không hợp lệ", 404
    return render_template( config['page_template'], **config, page_type=page_type )

@admin_bp.route('/<string:page_type>')
def comment(page_type):
    config = PAGE_CONFIG.get(page_type)
    if not config:
        return "Không hợp lệ", 404
    return render_template( config['page_template'], **config, page_type=page_type )

@admin_bp.route('/<string:page_type>')
def media(page_type):
    config = PAGE_CONFIG.get(page_type)
    if not config:
        return "Không hợp lệ", 404
    return render_template( config['page_template'], **config, page_type=page_type )