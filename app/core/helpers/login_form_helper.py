from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
class LoginFormHelper(FlaskForm):
    email = StringField("Nhập Email", validators=[DataRequired()])
    password = PasswordField("Nhập mật khẩu", validators=[DataRequired()])