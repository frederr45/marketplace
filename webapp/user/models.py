import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db
from webapp.message.models import Message


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mail = db.Column(db.String(50), index=True, unique=True)
    number = db.Column(db.String(11), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True, default='user')
    avatar = db.Column(db.String)
    street_address = db.Column(db.String)
    auto = db.relationship('Auto', lazy=True, backref='auto')
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'User {self.username}, id={self.id}'
