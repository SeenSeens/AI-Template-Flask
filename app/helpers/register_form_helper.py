from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email


class RegisterFormHelper(FlaskForm):
    username = StringField('Tên người dùng', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('Địa chỉ Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Nhập lại mật khẩu', validators=[
        DataRequired(),
        EqualTo('password', message='Mật khẩu không khớp')
    ])
    agree = BooleanField('Tôi đã đọc và đồng ý với Điều khoản & Điều kiện', validators=[DataRequired()])
    submit = SubmitField('Đăng ký')