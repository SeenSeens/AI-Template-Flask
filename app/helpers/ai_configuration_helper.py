from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class AIConfigurationHelper(FlaskForm):
    token = StringField(
        '🔐 API Token',
        validators=[
            DataRequired(message='Vui lòng nhập api token'),
        ]
    )
    provider = SelectField(
        '🤖 Chọn Provider',
        choices=[
            ('', 'Chọn Provider'),
            ('openai', 'OpenAI'),
            ("gemini", "Google"),
            ("anthropic", "Anthropic"),
            ("huggingface", "Huggingface"),
        ],
        validate_choice=False,
        validators=[
            DataRequired(message='Vui lòng chọn nhà cung cấp')
        ]
    )
    task_type = SelectField(
        '🔧 Loại tác vụ (Task)',
        choices=[
            ('', '-- Chọn loại tác vụ --'),
            ('text-generation', 'Text Generation'),
            ('text-classification', 'Text Classification'),
            ('summarization', 'Summarization'),
            ('text-to-image', 'Text to Image'),
            ('translation', 'Translation'),
            ('image-classification', 'Image Classification'),
            # Thêm task nào bạn cần
        ],
        validate_choice=False,
        default='text-generation'
    )
    model_name = SelectField(
        '📦 Model',
        choices=[('', '-- Chọn model --')],
        validate_choice=False,
        validators=[
            DataRequired(message='Vui lòng chọn model')
        ]
    )