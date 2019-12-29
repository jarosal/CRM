from flask import render_template, url_for, flash, redirect, request
from CRM import app, db, bcrypt
from CRM.models import User, Meeting
from CRM.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email = form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Konto stworzone dla {form.email.data}!', 'success')
        return redirect(url_for('dashboard')) #zmienic redirect na admin panel albo pozbyc sie wgl
    return render_template('register.html', title='Dodaj użytkownika', form=form)


@app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash('Zostałeś zalogowany!', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Logowanie nieudane. Proszę sprawdź podane dane.', 'danger')
#     return render_template('login.html', title='Zaloguj się', form=form)
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


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Konto')