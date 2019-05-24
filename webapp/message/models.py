import datetime
from webapp.db import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.body}>'
