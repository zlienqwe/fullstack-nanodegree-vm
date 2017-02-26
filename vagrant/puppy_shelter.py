import os
import sys
from sqlalchemy import Column, ForeignKey, String, Integer, Date, Boolean, Numeric

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()



class Shelter(Base):
	__tablename__ = 'shelter'
	id = Column(
		Integer, primary_key = True)
	name = Column(
		String(80), nullable = False)
	address = Column(
		String(250))
	city = Column(
		String(80))
	state = Column(
		String(20))
	zipCode = Column(
		String(10))
	website = Column(
		String)
	


class Puppy(Base):
	__tablename__ = 'puppy'
	id = Column(
		Integer, primary_key = True)
	name = Column(
		String(80), nullable = False)
	gender = Column(
		String(6), nullable = False)
	dateOfBirth = Column(
		Date)
	weight = Column(
		Numeric())
	shelter_id = Column(
		Integer, ForeignKey('shelter.id'))
	picture = Column(
		String)
	shelter = relationship(Shelter)


engine = create_engine(
	'sqlite:///puppy_shelter.db')
Base.metadata.create_all(engine)
