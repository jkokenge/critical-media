from .base import *
from os import environ

ROOT_URLCONF = "cml.cml.urls"

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ['NAME'],
        'USER': environ['USER'],
        'PASSWORD': environ['PASSWORD'],
        'HOST': environ['HOST'],
        'PORT': environ['PORT'],
    }
}


from cml.cml.settings.base import *
from mezzanine.utils.conf import set_dynamic_settings
set_dynamic_settings(globals())