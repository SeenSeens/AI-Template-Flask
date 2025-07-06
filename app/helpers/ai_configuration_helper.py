from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Label, SelectField, FloatField, BooleanField, FieldList
from wtforms.validators import DataRequired, NumberRange, InputRequired


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
    temperature = FloatField(
        '🎚️ Temperature',
        default=0.7,
        validators=[
            DataRequired(message='Vui lòng nhập temperature'),
            NumberRange(min=0.0, max=1.0, message='Giá trị phải nằm trong khoảng 0 đến 1')
        ]
    )
    max_tokens = FloatField(
        '🧠 Max Tokens',
        default=512,
        validators=[
            DataRequired(message='Vui lòng nhập max tokens'),
        ]
    )
    top_p = FloatField(
        '🎯 Top P',
        default=1.0,
        validators=[
            DataRequired(message='Vui lòng nhập top p'),
            NumberRange(min=0.0, max=1.0, message='Giá trị phải nằm trong khoảng 0 đến 1')
        ]
    )
    frequency_penalty = FloatField(
        '📉 Frequency Penalty',
        default=0.0,
        validators=[
            InputRequired(message='Vui lòng nhập frequency penalty'),
            NumberRange(min=0.0, max=2.0, message='Giá trị phải nằm trong khoảng 0 đến 2')
        ]
    )
    autocomplete = BooleanField('Autocomplete')
    summarize = BooleanField('Summarize')
    translate = BooleanField('Translate')
    multi_chat = BooleanField('Multi-turn Chat')
    features = FieldList(StringField(), default=[])  # nếu bạn dùng input hidden/checkbox