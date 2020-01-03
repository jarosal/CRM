from CRM import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    meetings = db.relationship('Meeting', backref='who', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.image_file}', '{self.name}', '{self.last_name}')"

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'),nullable=False)
    

    def __repr__(self):
        return f"Post('{self.notes}', '{self.date}')"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(25), nullable=False)
    agent_name = db.Column(db.String(35), nullable=False)
    agent_last_name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(140), nullable=False)
    phone = db.Column(db.String(140), nullable=False)
    address = db.Column(db.String(140), nullable=False)
    meetings = db.relationship('Meeting', backref='with_who', lazy=True)

    def __repr__(self):
        return f"Customer ('{self.customer_name}', '{self.agent_name}','{self.agent_last_name}', '{self.email}', '{self.phone}' , '{self.address}')"
        