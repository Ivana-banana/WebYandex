from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    type = StringField('Категория события', validators=[DataRequired()])
    content = TextAreaField("Описание")
    address = StringField('Адрес события', validators=[DataRequired()])
    submit = SubmitField('Применить')
