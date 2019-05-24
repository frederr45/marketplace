import datetime
from webapp.message.forms import MessageForm
from webapp.message.models import Message

from flask import Blueprint, render_template, redirect, url_for, \
    request, current_app, flash, jsonify
from flask_login import current_user, login_required

from webapp.market.models import Auto, Params, Images, Auto_brand,\
    Auto_models
from webapp.user.forms import RegistrationForm, LogoutForm
from webapp.db import db
from webapp.user.models import User

blueprint = Blueprint('message', __name__)


@blueprint.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(id=recipient).first_or_404()
    msgform = MessageForm()
    if msgform.validate_on_submit():
        new_msg = Message(
            sender_id=current_user.id,
            recipient_id=user.id,
            body=msgform.message.data)
        print(new_msg)
        db.session.add(new_msg)
        db.session.commit()
        flash('Ваше сообщение отправлено!')
        return redirect(url_for('market.index'))
    flash('Сообщение не отправлено')
    return redirect(url_for('market.index'))


@blueprint.route('/messages')
@login_required
def messages():
    form = RegistrationForm()
    logoutform = LogoutForm()
    current_user.last_message_read_time = datetime.datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    received_msg = Message.query.filter(
        Message.recipient_id == current_user.id).order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['MESSAGES_PER_PAGE'], False)
    
    next_url = url_for('message.messages', page=received_msg.next_num) \
        if received_msg.has_next else None
    prev_url = url_for('message.messages', page=received_msg.prev_num) \
        if received_msg.has_prev else None
    return render_template('message/messages.html',
                           received_msg=received_msg.items,
                           next_url=next_url, prev_url=prev_url, form=form,
                           logoutform=logoutform)



@blueprint.route('/sent_messages')
@login_required
def sent_messages():
    form = RegistrationForm()
    logoutform = LogoutForm()
    current_user.last_message_read_time = datetime.datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    sent_msg = Message.query.filter(
        Message.sender_id == current_user.id).order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['MESSAGES_PER_PAGE'], False)
    
    next_url = url_for('message.sent_messages', page=sent_msg.next_num) \
        if sent_msg.has_next else None
    prev_url = url_for('message.sent_messages', page=sent_msg.prev_num) \
        if sent_msg.has_prev else None
    return render_template('message/sent_messages.html',
                           next_url=next_url, prev_url=prev_url, form=form,
                           logoutform=logoutform, sent_msg=sent_msg.items)
