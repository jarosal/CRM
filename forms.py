from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class RegistrationForm(FlaskForm):
    # username = StringField('Username', Length(min=2, max=20))
    email = StringField('Email', validators=[InputRequired("Podaj adres email"), Email("Podaj poprawny adres email")])
    password = PasswordField('Hasło', validators=[InputRequired("Podaj hasło")])
    # confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Imię', validators=[InputRequired("Podaj imię")])
    last_name = StringField('Nazwisko', validators=[InputRequired("Podaj nazwisko")])
    submit = SubmitField('Dodaj')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired("Podaj adres email"), Email("Podaj poprawny adres email")])
    password = PasswordField('Hasło', validators=[InputRequired("Podaj hasło")])
    remember = BooleanField('Pamiętaj mnie')
    submit = SubmitField('Login')
