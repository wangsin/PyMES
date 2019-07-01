from flask import render_template, sessions, redirect, url_for
from . import main
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', user='not_login')


@main.route('/index', methods=['GET', 'POST'])
def index_two():
    return render_template('index.html', user='admin')


@main.route('/right', methods=['GET', 'POST'])
def right():
    return render_template('index.html', user='watcher')

