from flask import abort
from app.config.page_config import PAGE_CONFIG

def get_page_config(page_type, sub_type=None):
    config = PAGE_CONFIG.get(page_type)
    if not config:
        print(f"[DEBUG] Không tìm thấy config cho page_type: {page_type}")
        abort(404)

    if sub_type:
        sub_config = config.get(sub_type)
        if not sub_config:
            print(f"[DEBUG] Không tìm thấy sub_config cho sub_type: {sub_type} trong {page_type}")
            abort(404)
        return sub_config

    return config
