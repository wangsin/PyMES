from flask import current_app
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from . import login_manager

from app import db


@login_manager.user_loader
def login_user(user_id):
    return User.query.get(int(user_id))


def generate_pwd(pwd):
    return generate_password_hash(pwd)


class Material(db.Model):
    __tablename__ = 'Material'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(32), unique=True)
    rest = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = 'Order'
    order_id = db.Column(db.Integer, primary_key=True, unique=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    custom_id = db.Column(db.Integer, ForeignKey("Customer.id"))
    custom = relationship("Customer", backref="id_of_custom")
    is_available = db.Column(db.Boolean)
    is_finished = db.Column(db.Boolean)
    is_urgent = db.Column(db.Boolean)
    need_material = db.Column(db.Integer)
    need_material_id = db.Column(db.Integer, ForeignKey("Material.id"))
    material = relationship("Material", backref="id_of_material")
    need_stock = db.Column(db.Integer, default=6)


class Job(db.Model):
    __tablename__ = 'Job'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    order_id = db.Column(db.Integer, ForeignKey("Order.order_id"))
    order = relationship("Order", backref="id_of_order_1")
    input_path = db.Column(db.String(64))
    best_time = db.Column(db.Integer)
    best_aps = db.Column(db.String(128))
    best_solution = db.Column(db.String(128))
    result_img_path = db.Column(db.String(128))


class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64))
    tel = db.Column(db.String(32))
    company = db.Column(db.String(64))


class Stock(db.Model):
    __tablename__ = 'Stock'
    room_id = db.Column(db.Integer, primary_key=True, unique=True)
    rest_num = db.Column(db.Integer)
    full_num = db.Column(db.Integer)
    last_order = db.Column(db.Integer, ForeignKey("Order.order_id"))
    order = relationship("Order", backref="id_of_order_2")


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)
    simulate_num = db.Column(db.Integer)
    last_login = db.Column(db.DateTime)
    confirmed = db.Column(db.Boolean, default=False)
    is_administrator = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmd = True
        db.session.add(self)
        return True

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.name
