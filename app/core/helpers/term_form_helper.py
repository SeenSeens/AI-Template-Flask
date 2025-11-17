from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Optional


class TermFormHelper(FlaskForm):
    name = StringField(
        'Tên',
        render_kw={"placeholder": "Thêm tiêu đề", "class": "form-control"},
        validators=[DataRequired(message="Tên không được để trống")]
    )
    slug = StringField(
        'Slug',
        render_kw={"placeholder": "Đường dẫn", "class": "form-control"},
        validators=[
            DataRequired(message="Slug không được để trống"),
            Regexp(r'^[a-z0-9-]+$', message="Slug chỉ được chứa chữ thường, số và dấu gạch ngang")
        ]
    )
    description = TextAreaField(
        'Mô tả',
        render_kw={
            "placeholder": "Thêm nội dung",
            "class": "form-control",
            "rows": 10
        },
        validators=[Optional()]
    )