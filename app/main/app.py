from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:7251998MySql+@192.168.253.134/mes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    role = db.Column(db.Integer)
    email = db.Column(db.Integer, unique=True)

    def __repr__(self):
        print('<User:\n name:' + self.name + 'role:' + self.role + '\n')
        return '<User:\n name:' + self.name + 'role:' + self.role + '\n'


@app.route('/user-test/<name>')
def index_render(name):
    return render_template('index.html', name=name, date=datetime.date(datetime.now()))


@app.route('/login')
def login_render():
    return render_template('login.html')


@app.route('/db-test')
def db_render():
    return '<h1>'+repr(User)+'</h1>'


if __name__ == '__main__':
    app.run()
