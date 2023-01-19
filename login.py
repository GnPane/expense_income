from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username',
                           description='Логин от 6 до 30 символов',
                           validators=[DataRequired(message='Эта строка не должна быть пустой.'),
                                       Length(min=6, max=30, message="Логин должен быть от 6 до 30 символов.")
                                       ]
                           )
    password = PasswordField('Password',
                             validators=[DataRequired(message='Эта строка не должна быть пустой.'),
                                         Length(min=6, max=30, message="Пароль должен быть от 6 до 30 символов.")
                                         ]
                             )
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')