from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError
from CRM.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired("Podaj adres email"), Email("Podaj poprawny adres email")])
    password = PasswordField('Hasło', validators=[InputRequired("Podaj hasło")])
    name = StringField('Imię', validators=[InputRequired("Podaj imię")])
    last_name = StringField('Nazwisko', validators=[InputRequired("Podaj nazwisko")])
    submit = SubmitField('Dodaj')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Użytkownik z takim emailem już istnieje.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired("Podaj adres email"), Email("Podaj poprawny adres email")])
    password = PasswordField('Hasło', validators=[InputRequired("Podaj hasło")])
    remember = BooleanField('Pamiętaj mnie')
    submit = SubmitField('Login')