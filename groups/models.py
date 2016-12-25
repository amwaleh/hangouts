from mongoengine import *
import datetime
import os
# https://github.com/MongoEngine/mongoengine
# connect to the local mongodb if the name provided does not exist a new db is created with a similar names
CONN = "{}".format(os.getenv('MLAB_URL'))
connect(host=CONN)

class Groups(Document):
    '''
        This Document stores the list groups generated
        Fields:
            groups : Takes an iterable either a list or  tuple
            created: Auto created at the time of creating the document
    '''
    groups = ListField()
    created = DateTimeField(default=datetime.datetime.now)