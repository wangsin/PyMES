from flask import current_app
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
