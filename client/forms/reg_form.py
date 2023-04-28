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

def MyValidator(message):
    def _my_datarequired(form, field):
        data = field.data
        f1 = len(field.data) == 0
        if f1:
            raise ValidationError(message)

    return _my_datarequired

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


class RegForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[
                               MyValidator("Введите имя"),
                               user_check_check
                           ])

    email = StringField('Адрес электронной почты',
                        validators=
                        [
                            MyValidator("Введите почту"),
                            Email(message="Неправильная почта"),
                        ])

    password = PasswordField('Пароль',
                             validators=[
                                 MyValidator("Введите пароль"),
                                 Length(min=8,
                                        message='Пароль должен быть не короче 8 символов')])

    submit = SubmitField('Зарегистрироваться')
