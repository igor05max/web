from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


# регистрация
class RegistrationForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Ник пользователя', validators=[DataRequired()])

    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')
