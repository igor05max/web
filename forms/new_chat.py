from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


# начать общение
class NewChat(FlaskForm):
    message = TextAreaField("Сообщение")
    submit = SubmitField('Начать общение')
