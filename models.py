"""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class baseModel(db.Model):
	#base data model for all objects
	__abstract__ = True

	def __init__(self, *args):
		super().__init__(*args)
	def __repr__(self):
		return '%s(%s)' % (self.__class__.__name__, { column: value
			for column, value in self._todict().items()
		})

	def json(self):

		return {
			column: value if not isinstance(value, datetime.date) elseo"""	
