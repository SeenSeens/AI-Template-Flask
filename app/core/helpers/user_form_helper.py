from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class UserFormHelper(FlaskForm):
    username = StringField('Tên người dùng', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])

    role = SelectField('Vai trò', choices=[
        ('admin', 'Quản trị viên'),
        ('editor', 'Biên tập viên'),
        ('author', 'Tác giả'),
        ('subscriber', 'Người đăng ký')
    ], validators=[DataRequired()])

    status = SelectField('Trạng thái', choices=[
        ('active', 'Hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('banned', 'Bị cấm')
    ], validators=[DataRequired()])