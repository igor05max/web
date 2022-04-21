from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField


# редактирование комментария
class EditAComment(FlaskForm):
    comment = TextAreaField("Комментарий")
    submit = SubmitField('Редактировать')
