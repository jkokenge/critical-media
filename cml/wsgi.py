import os, sys
from os import environ


sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)))

print sys.path

from django.core.handlers.wsgi import WSGIHandler
DJANGO_SETTINGS_MODULE = environ['DJANGO_SETTINGS_MODULE']
#os.environ["DJANGO_SETTINGS_MODULE"] = "cml.settings"
application = WSGIHandler()