from dojo.connectdatabase import ConnectDatabase
from peewee import *


class Entries(Model):
    get_counter = IntegerField()
    post_counter = IntegerField()

    class Meta:
        database = ConnectDatabase.db
