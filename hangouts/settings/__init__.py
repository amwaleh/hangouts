from mongoengine import connect
from .base import *
DEBUG=True

if DEBUG:
    from .dev_settings import *
else:
    CONN = os.getenv('MLAB_URL')
    ALLOWED_HOSTS =['*']
