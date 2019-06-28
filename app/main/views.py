from flask import render_template

from forms import LoginForm
from . import main


@main.route('/', method=("GET", "POST"))
def index():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('auth/login.html', form=form)


@main.route('/user-test/<name>')
def show_name(name):
    return render_template('index.html', name=name)
