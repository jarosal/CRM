import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from CRM import app, db, bcrypt
from CRM.models import User, Meeting, Customer
from CRM.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddCustomerForm, MeetingForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/dashboard")
def dashboard():
    meetings = Meeting.query.all()
    return render_template('dashboard.html', meetings=meetings)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email = form.email.data, password = hashed_password, name = form.name.data, last_name = form.last_name.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Konto stworzone dla {form.email.data}!', 'success')
        return redirect(url_for('dashboard')) #zmienic redirect na admin panel albo pozbyc sie wgl
    return render_template('register.html', title='Dodaj użytkownika', form=form)


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
    meetings = Meeting.query.all()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, meetings=meetings)


@app.route("/add_customer", methods=['GET', 'POST'])
def add_customer():
    form = AddCustomerForm()
    if form.validate_on_submit():
        customer = Customer(email = form.email.data, customer_name = form.customer.data, agent_name = form.name.data, agent_last_name = form.last_name.data, phone = form.phone.data, address = form.address.data)
        db.session.add(customer)
        db.session.commit()
        flash(f'Konto stworzone dla {form.email.data}!', 'success')
        return redirect(url_for('dashboard')) # zmienic redirect na admin panel albo pozbyc sie wgl
    return render_template('add_customer.html', title='Dodaj użytkownika', form=form)

@app.route("/meetings", methods=['GET', 'POST'])
def meetings():
    meetings = Meeting.query.all()
    form = MeetingForm()
    if form.validate_on_submit():
        meeting = Meeting(who=current_user, with_who = Customer.query.filter_by(id=form.with_who.data).first()) # dodac date
        db.session.add(meeting)
        db.session.commit()
        flash('Spotkanie zostało dodane!', 'success')
        return redirect(url_for('meetings'))
    return render_template('meetings.html', meetings=meetings, form=form)

@app.route("/meetings/<int:meeting_id>")
def meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    return render_template('meeting.html', meeting=meeting)


@app.route("/meetings/<int:meeting_id>/update", methods=['GET', 'POST'])
#@login_required
def update_meeting(post_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    if meeting.who != current_user:
        abort(403)
    form = MeetingForm()
    if form.validate_on_submit():
        meeting.content = form.notes.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('meeting', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))