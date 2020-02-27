from peewee import *

db = SqliteDatabase('people.db')

class User(Model):
  chat_id = IntegerField()

  class Meta:
    database = db

class Leaf(Model):
  leaf_type = CharField()
  content = CharField()

  class Meta:
    database = db

class Story(Model):
  name = CharField()
  user = ForeignKeyField(User)

  class Meta:
    database = db

class Tree(Model):
  story = ForeignKeyField(Story)
  parent = ForeignKeyField(Leaf)
  child = ForeignKeyField(Leaf)

  class Meta:
    database = db

if db.connect():
  db.create_tables([User, Leaf, Story, Tree])