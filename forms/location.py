from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired


# создание локации и редактирование
class LocationForm(FlaskForm):
    file = MultipleFileField("")
    name_location = StringField('Название', validators=[DataRequired()])
    city = StringField('autocomplete_input', validators=[DataRequired()])
    category = StringField('Категория (памятник, музей, парк и т.д)', validators=[DataRequired()])
    about = TextAreaField("О месте")
    submit = SubmitField('Создать')
