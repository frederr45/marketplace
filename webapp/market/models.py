import datetime
from webapp.db import db


class Auto(db.Model):
    __tablename__ = 'auto'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, unique=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('auto_brand.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('auto_models.id'))
    images = db.relationship('Images', backref='auto', lazy=True)
    params = db.relationship('Params', backref='auto',
                             lazy=True, uselist=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<Auto {self.name} >'


class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    url_picture = db.Column(db.String, default='1200.jpg')


class Params(db.Model):
    __tablename__ = 'params'
    id = db.Column(db.Integer, primary_key=True)
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    holders = db.Column(db.String)
    generation = db.Column(db.String)
    condition = db.Column(db.String)
    steering_wheel = db.Column(db.String)
    wheeldrive = db.Column(db.String)
    color = db.Column(db.String)
    engine_capacity = db.Column(db.String)
    model = db.Column(db.String)
    mileage = db.Column(db.String)
    brand = db.Column(db.String)
    year = db.Column(db.String)
    body_type = db.Column(db.String)
    type_engine = db.Column(db.String)
    gear = db.Column(db.String)
    power = db.Column(db.String)
    doors = db.Column(db.String)
    vin = db.Column(db.String)
    location = db.Column(db.String)
    equipment = db.Column(db.String)
    modification = db.Column(db.String)


class Auto_brand(db.Model):
    __tablename__ = 'auto_brand'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    model = db.relationship('Auto_models', backref='auto_brand', lazy=True)
    auto_id = db.relationship('Auto', backref='auto_brand', lazy=True)


class Auto_models(db.Model):
    __tablename__ = 'auto_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    brand_id = db.Column(db.Integer, db.ForeignKey('auto_brand.id'))
    auto_id = db.relationship('Auto', backref='auto_models', lazy=True)

