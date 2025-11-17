from flask_wtf import FlaskForm
from wtforms import SelectField


class PostTermRelationshipsHelper(FlaskForm):
    category = SelectField('Danh mục', choices=[], coerce=int)
    tag = SelectField('Thẻ', choices=[], coerce=int)