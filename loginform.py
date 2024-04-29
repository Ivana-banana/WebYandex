from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    log1 = StringField('ID астронавта', validators=[DataRequired()])
    pas1 = PasswordField('Пароль астронавта', validators=[DataRequired()])
    log2 = StringField('ID капитана', validators=[DataRequired()])
    pas2 = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')