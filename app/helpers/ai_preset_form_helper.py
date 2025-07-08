from flask import json
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError


def validate_json(form, field):
    try:
        if field.data:
            json.loads(field.data)
    except ValueError:
        raise ValidationError("Nội dung phải là JSON hợp lệ.")

class AIPresetFormHelper(FlaskForm):
    use_case = StringField('Use case', validators=[DataRequired()])
    type = SelectField('Loại Preset',
        choices=[
            ('', 'Chọn Type'),
            ('content', 'Content'),
            ('image', 'Image'),
            ('design', 'Design'),
            ('audio', 'Audio'),
            ('video', 'Video'),
            ('other', 'Other')
        ],
        validate_choice=False,
        validators=[
           DataRequired(message='Vui lòng chọn loại Preset')
        ]
    )
    temperature = FloatField('Temperature', default=0.7, validators=[NumberRange(0, 2)])
    top_p = FloatField('Top P', default=1.0, validators=[NumberRange(0, 1)])
    max_tokens = IntegerField('Max Tokens', default=512)
    frequency_penalty = FloatField('Frequency Penalty', default=0.0, validators=[NumberRange(0, 2)])

    # Feature flags
    is_default = BooleanField('Đặt làm cấu hình mặc định')
    autocomplete = BooleanField('Tự động hoàn thành nội dung', default=True)
    summarize = BooleanField('Tóm tắt nội dung')
    translate = BooleanField('Dịch nội dung')
    multi_chat = BooleanField('Chat đa lượt (multi-turn)')

    features = TextAreaField(
        '🎯 Thông số bổ sung (JSON):',
        validators=[Optional(), validate_json],
        render_kw={
            "rows": 5,
            "class": "form-control",
            "placeholder": '''{
                "tone": "friendly",
                "language": "vi",
                "style": "blog",
                "output_format": "html"
            }'''
        }
    )
