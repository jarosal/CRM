from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from CRM.models import User, Customer, Meeting, Product, Contract, Supplier
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields.html5 import DateField, TimeField
from datetime import datetime



class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired("Podaj adres email"), Email("Podaj poprawny adres email")])
    password = PasswordField('Hasło', validators=[InputRequired("Podaj hasło")])
    name = StringField('Imię', validators=[InputRequired("Podaj imię")])
    last_name = StringField('Nazwisko', validators=[InputRequired("Podaj nazwisko")])
    admin = BooleanField('Administrator')
    submit = SubmitField('Dodaj')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Użytkownik z takim emailem już istnieje.')

class UpdateAccountForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Imię')
    last_name = StringField('Nazwisko')
    picture = FileField('Zmień zdjęcie', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Zapisz')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Użytkownik z takim emailem już istnieje.')

class EditAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Imię')
    last_name = StringField('Nazwisko')
    admin = BooleanField('Administrator')
    submit = SubmitField('Zapisz')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired("Podaj adres email"), Email("Podaj poprawny adres email")])
    password = PasswordField('Hasło', validators=[InputRequired("Podaj hasło")])
    remember = BooleanField('Pamiętaj mnie')
    submit = SubmitField('Login')




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
            raise ValidationError('Taki klient już istnieje.')
            
class EditCustomerForm(FlaskForm):
    customer = StringField('Nazwa firmy')
    name = StringField('Imię')
    last_name = StringField('Nazwisko')
    email = StringField('Email')
    phone = StringField('Telefon')
    address = StringField('Adres')
    submit = SubmitField('Zapisz')


class AddProductForm(FlaskForm):
    name = StringField('Nazwa', validators=[InputRequired("Podaj nazwę produktu")])
    price = IntegerField('Cena za kilogram', validators=[InputRequired("Podaj cenę produktu")])
    submit = SubmitField('Dodaj')

class EditProductForm(FlaskForm):

    name = StringField('Nazwa')
    price = IntegerField('Cena za kilogram')
    submit = SubmitField('Zapisz')


class MeetingForm(FlaskForm):

    def get_customers():      
        return Customer.query

    with_who = QuerySelectField('Klient', validators=[DataRequired()], query_factory=get_customers, get_label='customer_name')   # dodac date
    date = DateField('Data', format='%Y-%m-%d', default=datetime.utcnow)
    time = TimeField('Godzina', format='%H:%M', default=datetime.utcnow)
    title = StringField('Tytuł spotkania', validators=[InputRequired("Podaj tytuł spotkania")])
    submit = SubmitField('Dodaj')

class EditMeetingForm(FlaskForm):

    notes = TextAreaField('Notatki')
    submit = SubmitField('Zapisz')

class AddSupplierForm(FlaskForm):
    supplier = StringField('Nazwa firmy', validators=[InputRequired("Podaj nazwę firmy")])
    name = StringField('Imię', validators=[InputRequired("Podaj imię")])
    last_name = StringField('Nazwisko', validators=[InputRequired("Podaj nazwisko")])
    email = StringField('Email', validators=[InputRequired("Podaj adres email"), Email("Podaj poprawny adres email")])
    phone = StringField('Telefon', validators=[InputRequired("Podaj numer telefonu")])
    address = StringField('Adres', validators=[InputRequired("Podaj adres")])
    submit = SubmitField('Dodaj')

    def validate_supplier(self, supplier):
        supplier = Supplier.query.filter_by(supplier_name=supplier.data).first()
        if supplier:
            raise ValidationError('Taki dostawca już istnieje.')

class EditSupplierForm(FlaskForm):
    supplier = StringField('Nazwa firmy')
    name = StringField('Imię')
    last_name = StringField('Nazwisko')
    email = StringField('Email')
    phone = StringField('Telefon')
    address = StringField('Adres')
    submit = SubmitField('Zapisz')

class AddContractForm(FlaskForm):

    def get_products():      
        return Product.query
    
    def get_customers():      
        return Customer.query

    def get_suppliers():      
        return Supplier.query

    title = StringField('Tytuł umowy', validators=[InputRequired("Podaj tytuł umowy")])
    customer = QuerySelectField('Klient', validators=[DataRequired()], query_factory=get_customers, get_label='customer_name')
    supplier = QuerySelectField('Dostawca', validators=[DataRequired()], query_factory=get_suppliers, get_label='supplier_name')
    products = QuerySelectMultipleField('Produkty', validators=[DataRequired()], query_factory=get_products, get_label='name', option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=True))
    submit = SubmitField('Dodaj')


