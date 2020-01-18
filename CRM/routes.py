import os
import shutil
import secrets
import pandas as pd
import sqlite3
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from CRM import app, db, bcrypt
from CRM.models import User, Meeting, Customer, Product, Contract, Supplier, Products
from CRM.forms import RegistrationForm, LoginForm, AddProductForm, EditProductForm, UpdateAccountForm, AddCustomerForm, MeetingForm, EditMeetingForm, EditCustomerForm, AddSupplierForm, EditSupplierForm, EditAccountForm, AddContractForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import and_

def upcoming_meetings():
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day, datetime.today().hour)
    upcoming_meetings = Meeting.query.filter(and_(Meeting.date >= todays_datetime), Meeting.user_id == current_user.id ).all()
    return upcoming_meetings


    

@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    conn = sqlite3.connect("CRM\crm.db")
    df = pd.read_sql_query("select name,price from product;",conn)
    number_of_contracts = pd.read_sql_query("SELECT COUNT(id) from contract;",conn)
    value_of_contracts = pd.read_sql_query("SELECT SUM(value) from contract;",conn)
    users = pd.read_sql_query("select user.name,user.last_name,meeting.date from User inner join Meeting ON meeting.user_id=user.id",conn)
    users['who'] = users[['name', 'last_name']].apply(lambda x: ' '.join(x), axis=1)
    xd = users.to_html()

    # df.set_index('id', inplace=True)
    plot = df.plot.pie(y='price',autopct='%.2f',figsize=(5, 5))
    shutil.rmtree('CRM\static\plots')
    os.makedirs('CRM\static\plots')
    plot.figure.savefig('CRM\static\plots\my_plot2.png')
    return render_template('dashboard.html', meetings=upcoming_meetings(),number_of_contracts=number_of_contracts,value_of_contracts=value_of_contracts,users=users, xd=xd)

@app.route("/users", methods=['GET', 'POST'])
def users():
    form = RegistrationForm()
    users = User.query.all()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email = form.email.data, password = hashed_password, name = form.name.data, last_name = form.last_name.data, admin = form.admin.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Konto stworzone dla {form.email.data}!', 'success')
        return redirect(url_for('users'))
    return render_template('users.html', title='Użytkownicy', form=form, users=users)

@app.route("/users/<int:user_id>", methods=['GET', 'POST'])
# @login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditAccountForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.name = form.name.data
        user.last_name = form.last_name.data
        user.admin = form.admin.data
        db.session.commit()
        flash('Zmiany zapisane!', 'success')
        return redirect(url_for('user', user_id = user_id, meetings=upcoming_meetings()))

    elif request.method == 'GET':
        form.email.data = user.email
        form.name.data = user.name
        form.last_name.data = user.last_name
        form.admin.data = user.admin
    return render_template('user.html', user=user, form=form, meetings=upcoming_meetings())

@app.route("/users/<int:user_id>/delete", methods=['POST'])
# @login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user != user:
        db.session.delete(user)
        db.session.commit()
        flash('Użytkownik usunięty!', 'success')
    return redirect(url_for('users'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
#@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.last_name.data = current_user.last_name
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, meetings=upcoming_meetings())


@app.route("/customers", methods=['GET', 'POST'])
def customers():
    form = AddCustomerForm()
    customers = Customer.query.all()
    if form.validate_on_submit():
        customer = Customer(email = form.email.data, customer_name = form.customer.data, agent_name = form.name.data, agent_last_name = form.last_name.data, phone = form.phone.data, address = form.address.data)
        db.session.add(customer)
        db.session.commit()
        flash(f'Konto stworzone dla {form.email.data}!', 'success')
        return redirect(url_for('dashboard')) # zmienic redirect na admin panel albo pozbyc sie wgl
    return render_template('customers.html', title='Dodaj użytkownika', form=form, customers=customers)

@app.route("/customers/<int:customer_id>", methods=['GET', 'POST'])
# @login_required
def customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = EditCustomerForm()
    if form.validate_on_submit():
        customer.email = form.email.data 
        customer.customer_name = form.customer.data
        customer.agent_name = form.name.data
        customer.agent_last_name = form.last_name.data
        customer.phone = form.phone.data
        customer.address = form.address.data
        db.session.commit()
        flash('Zmiany zapisane!', 'success')
        return redirect(url_for('customer', customer_id = customer_id, meetings=upcoming_meetings()))

    elif request.method == 'GET':
        form.email.data = customer.email
        form.customer.data = customer.customer_name
        form.name.data = customer.agent_name
        form.last_name.data = customer.agent_last_name
        form.phone.data = customer.phone
        form.address.data = customer.address
    return render_template('customer.html', customer=customer, form=form, meetings=upcoming_meetings())

@app.route("/customers/<int:customer_id>/delete", methods=['POST'])
# @login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash('Klient usunięty!', 'success')
    return redirect(url_for('customers'))


@app.route("/products" ,methods=['GET', 'POST'])
def products():

    form = AddProductForm()
    if form.validate_on_submit():
        product_to_add = Product(name = form.name.data, price = form.price.data)
        db.session.add(product_to_add)
        db.session.commit()
        flash(f'Produkt dodany!', 'success')
        return redirect(url_for('products'))

    product = Product.query.all()
    return render_template('products.html', product=product, form=form)

@app.route("/products/<int:product_id>", methods=['GET', 'POST'])
# @login_required
def product(product_id):
    product = Product.query.get_or_404(product_id)
    form = EditProductForm()
    if form.validate_on_submit():
        product.name = form.name.data 
        product.price = form.price.data
        db.session.commit()
        flash('Zmiany zapisane!', 'success')
        return redirect(url_for('product', product_id = product_id, meetings=upcoming_meetings()))

    elif request.method == 'GET':
        form.name.data = product.name  
        form.price.data = product.price
    return render_template('product.html', product=product, form=form, meetings=upcoming_meetings())

@app.route("/products/<int:product_id>/delete", methods=['POST'])
# @login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product usunięty!', 'success')
    return redirect(url_for('products'))


@app.route("/contracts", methods=['GET', 'POST'])

def contracts():
    form = AddContractForm()
    contracts = Contract.query.filter(Contract.user_id == current_user.id).all()
    if form.validate_on_submit():
        contract = Contract(user = current_user, customer = form.customer.data, supplier = form.supplier.data, title = form.title.data, value = form.value.data)
        for product in form.products.data:
            prod = Products(products = contract, contract = product)
            db.session.add(prod)
        db.session.add(contract)
        db.session.commit()
        flash('Umowa dodana!', 'success')
        return redirect(url_for('contracts'))
    return render_template('contracts.html', form=form, contracts=contracts)

@app.route("/contracts/<int:contract_id>", methods=['GET', 'POST'])
# @login_required
def contract(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    products = Products.query.filter(Products.contract_id == contract_id).all()
    return render_template('contract.html', contract=contract, meetings=upcoming_meetings(), products=products)






@app.route("/meetings", methods=['GET', 'POST'])
# @login_required
def meetings():
    form = MeetingForm()
    meetings = Meeting.query.filter(Meeting.user_id == current_user.id).all()
    if form.validate_on_submit():
        meeting = Meeting(who = current_user, with_who = Customer.query.filter_by(id=form.with_who.data.id).first(), date = datetime.combine(form.date.data, form.time.data), title = form.title.data, typ = form.typ.data)
        db.session.add(meeting)
        db.session.commit()
        flash('Zdarzenie zostało dodane!', 'success')
        return redirect(url_for('meetings'))
    return render_template('meetings.html', meetings=meetings, form=form)

@app.route("/meetings/<int:meeting_id>", methods=['GET', 'POST'])
# @login_required
def meeting(meeting_id):
    form = EditMeetingForm()
    meeting = Meeting.query.get_or_404(meeting_id)
    if form.validate_on_submit():
        meeting.notes = form.notes.data
        db.session.commit()
        flash('Zmiany zapisane!', 'success')
        return redirect(url_for('meeting', meeting_id = meeting_id, meetings=upcoming_meetings()))
    elif request.method == 'GET':
        form.notes.data = meeting.notes
    return render_template('meeting.html', meeting=meeting, form=form, meetings=upcoming_meetings())


@app.route("/meetings/<int:meeting_id>/delete", methods=['POST'])
# @login_required
def delete_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    if meeting.who != current_user:
        abort(403)
    db.session.delete(meeting)
    db.session.commit()
    flash('Zdarzenie usunięte!', 'success')
    return redirect(url_for('meetings'))


@app.route("/suppliers", methods=['GET', 'POST'])
def suppliers():
    form = AddSupplierForm()
    suppliers = Supplier.query.all()
    if form.validate_on_submit():
        supplier = Supplier(email = form.email.data, supplier_name = form.supplier.data, supplier_agent_name = form.name.data, supplier_agent_last_name = form.last_name.data, phone = form.phone.data, address = form.address.data)
        db.session.add(supplier)
        db.session.commit()
        flash(f'Dostawca dodany', 'success')
        return redirect(url_for('suppliers'))
    return render_template('suppliers.html', title='Dostawcy', form=form,suppliers=suppliers)

@app.route("/suppliers/<int:supplier_id>", methods=['GET', 'POST'])
# @login_required
def supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    form = EditSupplierForm()
    if form.validate_on_submit():
        supplier.email = form.email.data 
        supplier.supplier_name = form.supplier.data
        supplier.supplier_agent_name = form.name.data
        supplier.supplier_agent_last_name = form.last_name.data
        supplier.phone = form.phone.data
        supplier.address = form.address.data
        db.session.commit()
        flash('Zmiany zapisane!', 'success')
        return redirect(url_for('supplier', supplier_id = supplier_id, meetings=upcoming_meetings()))

    elif request.method == 'GET':
        form.email.data = supplier.email
        form.supplier.data = supplier.supplier_name
        form.name.data = supplier.supplier_agent_name
        form.last_name.data = supplier.supplier_agent_last_name
        form.phone.data = supplier.phone
        form.address.data = supplier.address
    return render_template('supplier.html', supplier=supplier, form=form, meetings=upcoming_meetings())

@app.route("/suppliers/<int:supplier_id>/delete", methods=['POST'])
# @login_required
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    flash('Dostawca usunięty!', 'success')
    return redirect(url_for('suppliers'))




