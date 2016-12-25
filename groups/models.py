from mongoengine import *
import datetime
# https://github.com/MongoEngine/mongoengine
# connect to the local mongodb
connect('local')

class Groups(Document):
    '''
        This Document stores the list groups generated
        Fields:
            groups : Takes an iterable either a list or  tuple
            created: Auto created at the time of creating the document
    '''
    groups = ListField()
    created = DateTimeField(default=datetime.datetime.now)