import datetime
import os
import random
import time

from flask import render_template, flash, redirect
from flask_login import current_user, login_required

from app.analysis.analysis_excel import resolve_excel
from app.anti_heat_jsp.calculate import calculate_result
from app.models import User, Material, Order, Customer, Job, Stock
from forms import AddMaterial, AddOrderForm, AddCustomer, AddJob, StartWatchForm, AddStock
from . import main
from .. import db

t = time.time()

id = 0


@main.route('/', methods=['GET', 'POST'])
def index_render():
    return render_template('index.html')


@main.route('/users', methods=['GET', 'POST'])
@login_required
def user_manager():
    if not current_user.is_administrator:
        return render_template('error/401.html')

    return render_template('user/users.html', users=db.session.query(User.id, User.name, User.email, User.is_administrator))


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
    return render_template('material/material.html', form=form, materials=db.session.query(Material.id, Material.name, Material.rest))


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
    return render_template('order/order.html', form=form, orders=db.session.query(Order.order_id, Order.start_date
                                                                                  , Order.end_date, Order.custom_id
                                                                                  , Order.is_available, Order.is_finished,
                                                                                  Order.is_urgent, Order.need_material_id, Order.need_material, Order.need_stock))


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

    return render_template('customer.html', form=form, customers=db.session.query(Customer.id, Customer.name, Customer.tel, Customer.company))


@main.route('/stock', methods=['GET', 'POST'])
@login_required
def manage_stock():
    if not current_user.is_administrator:
        return render_template('error/401.html')
    form = AddStock()
    if form.validate_on_submit():
        stock = Stock(room_id=int(t + random.randint(0, 10)),
                      rest_num=form.rest_num.data,
                      full_num=form.full_num.data)

        db.session.add(stock)
        db.session.commit()
        flash('仓库注册成功')

    return render_template('stock/stock.html', form=form
                           , stocks=db.session.query(Stock.room_id, Stock.rest_num, Stock.full_num))


@main.route('/watcher', methods=['GET', 'POST'])
@login_required
def watch_job():
    form = StartWatchForm()
    job_id = form.job_id.data
    watch_arr = []
    if form.validate_on_submit():
        watch_arr.append(Job.query.filter_by(id=job_id).first().best_time)
        watch_arr.append(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M'))
        watch_arr.append(datetime.datetime.strftime(datetime.datetime.now() +
                                                    datetime.timedelta(minutes=watch_arr[0]), '%Y-%m-%d %H:%M'))
        watch_arr.append(Order.query.filter_by(order_id=Job.query.filter_by(id=job_id).first().order_id).first().need_stock)

    return render_template('watcher/watcher.html'
                           , form=form, id=job_id, arr=watch_arr)


@main.route('/simulate', methods=['GET', 'POST'])
@login_required
def simulate_job():
    global id
    if not current_user.is_administrator:
        return render_template('error/401.html')
    form = AddJob()
    if form.validate_on_submit():
        order_id = form.order_id.data
        if Order.query.filter_by(order_id=order_id).first():
            upload_file = form.upload_file.data
            upload_file_path = '/Projects/PyCharm/PyMES/app/static/xls/job_time' + int(
                t).__str__() + upload_file.filename
            upload_file.save(upload_file_path)
            context, init_solution = resolve_excel(upload_file_path)
            id = calculate_result(upload_file_path, context, init_solution, order_id)
            flash('上传成功，并且成功开始模拟')
        else:
            flash('请输入准确的订单号！')

    result = Job.query.filter_by(id=id).first()
    return render_template('simulate/simulate.html', form=form, result=result)


@main.route('/query-job', methods=['GET', 'POST'])
def query_job():
    return render_template('watcher/query_job.html', jobs=db.session.query(Job.id, Job.order_id
                                                                           , Job.best_time, Job.best_aps))

