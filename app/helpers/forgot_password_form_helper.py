from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired, Email


class ForgotPasswordFormHelper(FlaskForm):
    email = EmailField('Địa chỉ email', validators=[DataRequired(), Email()])
    submit = SubmitField('Gửi')