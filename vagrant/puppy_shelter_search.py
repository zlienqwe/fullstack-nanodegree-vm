from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from puppy_shelter import Base, Puppy, Shelter
import datetime


engine = create_engine('sqlite:///puppy_shelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


for puppy in session.query(Puppy).order_by(Puppy.name.asc()):
	print puppy.name

now = datetime.datetime.now()

def compairAge(compairMonth, birthday):
	year = now.year
	month = now.month
	day = now.day
	if now.month > compairMonth + 1:
		month = now.month - 6
	else:
		month = 12 - (compairMonth - now.month)
		year = now.year - 1
	return str(birthday) > str(year)+'-'+'%(month)02d'%{'month':month}+'-'+str(day)



for puppy in session.query(Puppy).all():

	if compairAge(6, puppy.dateOfBirth):
		print puppy.dateOfBirth
	else:
		print 'not'+str(puppy.dateOfBirth)


for puppy in session.query(Puppy).order_by(Puppy.weight.asc()):
	print puppy.weight



# for shelter in session.query(Shelter).all():
# for puppy_shelter in session.query(Puppy).group_by(Puppy.shelter_id).all():
	# for i in puppy_shelter:
		# print i

# for item in session.query(Shelter, func.count(Puppy.id)).group_by(Puppy.shelter_id).all():
# 	print item[0].name

# result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
# for item in result:
# 	print item[0].id, item[0].name, item[1]


# result = session.query(Puppy.shelter_id, Shelter.name, func.count(Puppy.id)).group_by(Puppy.shelter_id).all()
# for re in result:
# 	print re




