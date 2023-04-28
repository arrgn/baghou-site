from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import ValidationError


def my_length_check(form, field):
    data = field.data
    f1 = len(data) < 8
    if f1:
        raise ValidationError('Пароль должен быть не короче 8 символов')


def email_check(form, field):
    pass


def user_check_check(form, field):
    data = field.data
    f1 = len(data) > 12
    f2 = len(data) < 2
    f3 = False
    st = "_"
    for i in list(data):
        if not (i.isalnum() or i in st):
            f3 = True

    if f1:
        raise ValidationError('Имя должно быть короче 12 символов')
    if f2:
        raise ValidationError('Имя должно быть длиннее 2 символов')
    if f3:
        raise ValidationError('Имя содержит недопустимые символы')
    pass


class LoginForm(FlaskForm):
    email = StringField('Адрес электронной почты',
                        validators=
                        [
                            DataRequired(),
                            Email(message="Неправильная почта"),
                        ])

    password = PasswordField('Пароль',
                             validators=[
                                 DataRequired(),
                                 Length(min=8,
                                        message='Пароль должен быть не короче 8 символов')])

    submit = SubmitField('Войти')
