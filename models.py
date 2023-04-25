import configparser
from mongoengine import *


config = configparser.ConfigParser()
config.read('config.ini')

mongo_url = config.get('DB', 'URI')

connect(host=mongo_url, ssl=True)


class Author(Document):
    fullname = StringField(max_length=120, required=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=200)
    description = StringField()


class Quote(Document):
    tags = ListField(StringField(max_length=200))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {'allow_inheritance': True}