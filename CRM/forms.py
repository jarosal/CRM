from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError
from CRM.models import User, Customer, Meeting
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField, TimeField
from datetime import datetime



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

class UpdateAccountForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class AddCustomerForm(FlaskForm):
    customer = StringField('Nazwa firmy', validators=[InputRequired("Podaj nazwę firmy")])
    name = StringField('Imię', validators=[InputRequired("Podaj imię")])
    last_name = StringField('Nazwisko', validators=[InputRequired("Podaj nazwisko")])
    email = StringField('Email', validators=[InputRequired("Podaj adres email"), Email("Podaj poprawny adres email")])
    phone = StringField('Telefon', validators=[InputRequired("Podaj numer telefonu")])
    address = StringField('Adres', validators=[InputRequired("Podaj adres")])
    submit = SubmitField('Dodaj')

    def validate_customer(self, customer):
        customer = Customer.query.filter_by(customer_name=customer.data).first()
        if customer:
            raise ValidationError('Taka firma już istnieje.')


class MeetingForm(FlaskForm):

    def get_customers():      
        return Customer.query

    with_who = QuerySelectField('Klient', validators=[DataRequired()], query_factory=get_customers, get_label='customer_name')   # dodac date
    date = DateField('Data', format='%Y-%m-%d', default=datetime.utcnow)
    time = TimeField('Godzina', format='%H:%M', default=datetime.utcnow)
    submit = SubmitField('Dodaj')
