from peewee import *

class User():
	chat_id = IntegerField()

class Leaf():
	type = CharField()
  content = CharField()

class Story():
	name = CharField()
	user = ForeignKeyField(User)

class Tree():
	story = ForeignKeyField(Story)
	parent = ForeignKeyField(Leaf)
  child = ForeignKeyField(Leaf)
