import logging

from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user, login_required

from webapp.user.forms import RegistrationForm, LoginForm, LogoutForm
from webapp.message.forms import MessageForm
from webapp.db import db
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/id_<id>')
@login_required
def user_account(id):
    title = 'Профиль'
    form = LoginForm()
    regform = RegistrationForm()
    logoutform = LogoutForm()
    msgform = MessageForm()
    user = User.query.filter_by(id=id).first()
    return render_template('user/account.html', user=user, page_title=title,
                           form=form, regform=regform,
                           logoutform=logoutform, msgform=msgform)


@blueprint.route('/login', methods=['POST'])
def process_login():
    if current_user.is_authenticated:
        return redirect(url_for('market.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Вы вошли! Привет {user.name}!')
            logging.info(f'Зашел пользователь с id={user.id}')
            return redirect(url_for('market.index'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('market.index'))


@blueprint.route('/process_registration', methods=['POST'])
def process_registration():
    if current_user.is_authenticated:
        return redirect(url_for('market.index'))
    regform = RegistrationForm()
    if regform.validate_on_submit():
        new_user = User(number=f'8{regform.number.data}',
                        mail=regform.mail.data,
                        name=regform.name.data,
                        role='user'
                        )
        new_user.set_password(regform.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Вы успешно зарегистрировались!')
        logging.info(f'Новый пользователь с id={new_user.id}')
        return redirect(url_for('market.index'))
    else:
        for field, errors in regform.errors.items():
            for error in errors:
                flash(
                 f"В поле {getattr(regform, field).label.text}: -{error}")
        return redirect(url_for('market.registration'))


@blueprint.route('/logout', methods=['POST'])
def logout():
    logging.info(f'Вышел пользователь с id={current_user.id}')
    logout_user()
    flash('Вы вышли из аккаунта!')
    return redirect(url_for('market.index'))

