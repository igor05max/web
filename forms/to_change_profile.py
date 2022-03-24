from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class To_changeForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    name = StringField('Ник пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Изменить')
