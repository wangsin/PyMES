from werkzeug.security import generate_password_hash, check_password_hash
from app.main import db


class User(db.Model):

    Name = db.Column(db.String(64), unique=True)
    Id = db.Column(db.Integer(11), primary_key=True, unique=True)
    Password = db.Column(db.String(64))
    Email = db.Column(db.String(64), unique=True)
    Role = db.Column(db.Integer(11))
    SimulateNum = db.Column(db.Integer(11))
    LastLogin = db.Column(db.DateTime())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.Password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.Password, password)