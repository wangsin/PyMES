from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user

from app import db
from app.models import User
from .forms import LoginForm, RegistrationForm
from . import auth
from ..models import generate_pwd

import time
import random

t = time.time()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash("用户不存在")
        elif user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startwith('/'):
                next = url_for('main.index')
            flash("登陆成功")
        else:
            flash("账号或密码错误")
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("你已经成功登出")
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(id=int(t) + random.randint(0, 10),
                    email=form.email.data,
                    name=form.username.data,
                    password=generate_pwd(form.password.data),
                    is_administrator=form.is_administrator.data)
        db.session.add(user)
        db.session.commit()
        flash('您现在可以登陆了')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
