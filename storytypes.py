from peewee import *

db = SqliteDatabase('people.db')

class Entity():
   class Meta:
        database = db

class User(Entity):
  chat_id = IntegerField()

class Leaf(Entity):
  leaf_type = CharField()
  content = CharField()

class Story(Entity):
  name = CharField()
  user = ForeignKeyField(User)

class Tree(Entity):
  story = ForeignKeyField(Story)
  parent = ForeignKeyField(Leaf)
  child = ForeignKeyField(Leaf)
