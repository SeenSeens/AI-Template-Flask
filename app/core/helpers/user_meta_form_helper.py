from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional, DataRequired, Email


class UserMetaFormHelper(FlaskForm):
    username = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    mobile = StringField('Mobile', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    submit = SubmitField('Save Changes')