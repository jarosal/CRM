from CRM import db
db.drop_all()
db.create_all()

from CRM.models import User, Customer

user = User(email = 'admin@egjs.pl', name = 'Jarosław', last_name = 'Śliwiński', password = '$2b$12$Gm3Of9kRyShD3bxLuArsLOzpZfPwip7T.hJMZL5QDLplaIuto2wAO')
# hasło to 123

customer1 = Customer(customer_name = 'Tesco', agent_name = 'Emil', agent_last_name = 'Gugała', email = 'gugson@xd.pl', phone = '123123123', address = 'Głogówno')
customer2 = Customer(customer_name = 'Biedronka', agent_name = 'Paweł', agent_last_name = 'Graczyk', email = 'coolguy@speedgraczyk.pl', phone = '123123123', address = 'Głogówno')

db.session.add(user)
db.session.add(customer1)
db.session.add(customer2)
db.session.commit()