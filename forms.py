from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


##WTForm
class CreateList(FlaskForm):
    list_item = StringField("", validators=[DataRequired()])


