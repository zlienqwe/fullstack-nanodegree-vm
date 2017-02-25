from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for item in veggieBurgers:
	print str(item.id) + '\n' + item.name + '\n' + item.price + '\n\n'
	item.price = '$8.88'
	session.delete(item)

session.commit()

for item in veggieBurgers:
	print str(item.id) + '\n' + item.name + '\n' + item.price + '\n\n'



