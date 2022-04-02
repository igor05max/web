from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, MultipleFileField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class LocationForm(FlaskForm):
    file = MultipleFileField("")
    name_location = StringField('Название места', validators=[DataRequired()])
    about = TextAreaField("О месте")
    submit = SubmitField('Создать')
