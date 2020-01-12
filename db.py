from CRM import db
db.drop_all()
db.create_all()

from CRM.models import User, Customer, Supplier, Product

user = User(email = 'admin@egjs.pl', name = 'Jarosław', last_name = 'Śliwiński', password = '$2b$12$Gm3Of9kRyShD3bxLuArsLOzpZfPwip7T.hJMZL5QDLplaIuto2wAO', admin = True)
# hasło to 123

customer1 = Customer(customer_name = 'Tesco', agent_name = 'Emil', agent_last_name = 'Gugała', email = 'gugson@xd.pl', phone = '123123123', address = 'Głogówno')
customer2 = Customer(customer_name = 'Biedronka', agent_name = 'Paweł', agent_last_name = 'Graczyk', email = 'coolguy@speedgraczyk.pl', phone = '123123123', address = 'Głogówno')

supplier1 = Supplier(supplier_name = 'Dostawca1', supplier_agent_name = 'Emil', supplier_agent_last_name = 'Gugała', email = 'gugson@xd.pl', phone = '123123123', address = 'Głogówno')
supplier2 = Supplier(supplier_name = 'Dostawca2', supplier_agent_name = 'Emil', supplier_agent_last_name = 'Gugała', email = 'gugson@xd.pl', phone = '123123123', address = 'Głogówno')

product1 = Product(name = "Banan", price = 2)
product2 = Product(name = "Jabłko", price = 1)

db.session.add(user)
db.session.add(customer1)
db.session.add(customer2)
db.session.add(supplier1)
db.session.add(supplier2)
db.session.add(product1)
db.session.add(product2)
db.session.commit()