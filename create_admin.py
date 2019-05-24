from getpass import getpass
import sys
from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app()

with app.app_context():
    number = input('Введите номер телефона: ')

    if len(number) != 10:
        print('Номер вводится без 8 и должен состоять из 10 цифр')
        sys.exit(0)

    if User.query.filter(User.number == number).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    mail = input('Введите mail: ')
    name = input('Введите имя пользователя: ')

    if User.query.filter(User.mail == mail).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(number=f'8{number}', mail=mail,
                    name=name, role='admin')
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print(f'Создан пользователь с id={new_user.id}')
