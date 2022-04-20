from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField


class NewChat(FlaskForm):
    message = TextAreaField("Сообщение")
    submit = SubmitField('Начать общение')
