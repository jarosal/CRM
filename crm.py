from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '15f745100028f7f415b74e9fd7ac7c7f'

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
        flash(f'Konto stworzone dla {form.email.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', title='Dodaj użytkownika', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Zostałeś zalogowany!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Logowanie nieudane. Proszę sprawdź podane dane.', 'danger')
    return render_template('login.html', title='Zaloguj się', form=form)


