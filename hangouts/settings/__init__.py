from .base import *

DEBUG =bool(os.getenv('DEBUG',False))
if DEBUG:
    from .dev_settings import *
else:
    CONN = os.getenv('MLAB_URL')
    ALLOWED_HOSTS = ['*']

