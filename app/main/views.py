import random
import time

from flask import render_template, flash
from flask_login import current_user, login_required

from app.models import User, Material, Order, Customer
from forms import AddMaterial, AddOrderForm, AddCustomer
from . import main
from .. import db

t = time.time()


@main.route('/', methods=['GET', 'POST'])
def index_render():
    return render_template('index.html')


@main.route('/users', methods=['GET', 'POST'])
@login_required
def user_manager():
    if not current_user.is_administrator:
        return render_template('error/401.html')

    return render_template('users.html', users=db.session.query(User.id, User.name, User.email, User.is_administrator))


@main.route('/material', methods=['GET', 'POST'])
@login_required
def manage_material():
    if not current_user.is_administrator:
        return render_template('error/401.html')

    form = AddMaterial()
    if form.validate_on_submit():
        material = Material(id=int(t) + random.randint(0, 10),
                            name=form.name.data,
                            rest=form.rest.data)
        db.session.add(material)
        db.session.commit()
        flash('物料添加成功')
    return render_template('material.html', form=form)


@main.route('/order', methods=['GET', 'POST'])
@login_required
def manage_order():
    if not current_user.is_administrator:
        return render_template('error/401.html')

    form = AddOrderForm()
    if form.validate_on_submit():
        order = Order(order_id=int(t) + random.randint(0, 10),
                      start_date=form.start_date.data,
                      custom_id=Customer.query.filter_by(tel=form.customer_tel.data).first_or_404().id,
                      is_available=True,
                      is_finished=False,
                      is_urgent=form.is_urgent.data,
                      need_material=form.need_material.data,
                      need_material_id=Material.query.filter_by(id=form.need_material_id.data).first_or_404().id,
                      need_stock=form.need_stock.data)
        db.session.add(order)
        db.session.commit()
        flash('订单添加成功')
    return render_template('order.html', form=form)


@main.route('/customer', methods=['GET', 'POST'])
@login_required
def manage_customer():
    if not current_user.is_administrator:
        return render_template('error/401.html')

    form = AddCustomer()
    if form.validate_on_submit():
        customer = Customer(id=int(t) + random.randint(0, 10),
                            name=form.customer_name.data,
                            tel=form.customer_tel.data,
                            company=form.customer_company.data)

        db.session.add(customer)
        db.session.commit()
        flash('订单注册成功')

    return render_template('customer.html', form=form)
