from peewee import SqliteDatabase, CharField, ForeignKeyField, Model, IntegerField

db = SqliteDatabase('stories.db')

class Leaf(Model):
    leaf_type = CharField()
    content = CharField()

    class Meta:
        database = db


class Story(Model):
    name = CharField()
    chat_id = IntegerField()

    class Meta:
        database = db


class Tree(Model):
    story = ForeignKeyField(Story)
    parent = ForeignKeyField(Leaf)
    child = ForeignKeyField(Leaf)

    class Meta:
        database = db


if db.connect():
    db.create_tables([Leaf, Story, Tree])
    db.close()
