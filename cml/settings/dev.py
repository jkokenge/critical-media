from os import environ
import os

ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

DEBUG = True

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

from cml.settings.base import *
from mezzanine.utils.conf import set_dynamic_settings
set_dynamic_settings(globals())
