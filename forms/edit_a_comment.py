from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class EditAComment(FlaskForm):
    comment = TextAreaField("Комментарий")
    submit = SubmitField('Редактировать')
