from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostFormHelper(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    slug = StringField('Đường dẫn', validators=[DataRequired()])
    content = TextAreaField('Nội dung')
    excerpt = TextAreaField('Tóm tắt')
    submit_draft = SubmitField('Lưu nháp')