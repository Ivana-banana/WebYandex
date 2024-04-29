from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    age = IntegerField('Возраст пользователя', validators=[DataRequired()])
    phone = StringField('Телефон пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    sex = StringField('Пол', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегестрироваться')