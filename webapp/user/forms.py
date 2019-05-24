from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
                               ValidationError

from webapp.user.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()],
                           render_kw={"class": "form-control",
                                      "placeholder": "Введите Ваше имя"})
    number = StringField('Номер телефона', validators=[
        DataRequired(),
        Length(
            min=10,
            max=10,
            message="Номер очень короткий, введите 10 цифр")],
                             render_kw={"class": "form-control",
                                        "maxlength": 10,
                                        "placeholder": "1234567890",
                                        })
    mail = StringField('Почта', validators=[
        DataRequired(),
        Email(
            message="Введите правильный электронный адрес"
        )],
                            render_kw={"class": "form-control",
                                       "placeholder": "example@mail.ru"})
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(
            min=8,
            max=32,
            message="Пароль должен быть минимум 8 символов")],
                             render_kw={"class": "form-control"})
    password2 = PasswordField(
        'Повторите пароль', 
        validators=[
            DataRequired(),
            Length(min=8,
                   max=32,
                   message="Пароль должен быть минимум 8 символов"),
            EqualTo(
                'password',
                message="Пароли не совпадают")],
        render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня', default=True,
                               render_kw={"class": "form-check-input"})
    submit = SubmitField('Зарегестрироваться',
                         render_kw={"class": "btn btn-success"})

    def validate_email(self, user_mail):
        form = RegistrationForm()
        user_count = User.query.filter_by(
            user_mail=form.user_mail.data).count()
        if user_count > 0:
            raise ValidationError('Такая почта уже зарегистрирована')

    def validate_tel(self, tel_number):
        form = RegistrationForm()
        if len(form.tel_number.data) == 10:
            user_count = User.query.filter_by(
                tel_number=form.tel_number.data).count()
            if user_count > 0:
                raise ValidationError('Этот номер уже зарегистрирован')
        raise ValidationError('Введите правильный номер')


class LoginForm(FlaskForm):
    mail = StringField('Почта', validators=[
        DataRequired(),
        Email(
            message="Введите правильный электронный адрес"
        )],
                            render_kw={"class": "form-control",
                                       "placeholder": "example@mail.ru"})
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(
            min=8,
            max=32,
            message="Пароль должен быть минимум 8 символов")],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Войти',
                         render_kw={"class": "btn btn-success"})
    remember_me = BooleanField('Запомнить меня', default=True,
                               render_kw={"class": "form-check-input"})


class LogoutForm(FlaskForm):
    choice_yes = SubmitField('Выйти',  render_kw={"class": "btn btn-danger"})

