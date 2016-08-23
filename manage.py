#!/usr/bin/env python

# When project_template is used as the actual project during Mezzanine
# development, insert the development path into sys.path so that the
# development version of Mezzanine is used rather than the installed
# version.
import os
from os import environ
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)))

project_path = os.path.dirname(os.path.abspath(__file__))
project_dir = project_path.split(os.sep)[-1]
if project_dir == "project_template":
    dev_path = os.path.abspath(os.path.join(project_path, "..", ".."))
    if dev_path not in sys.path:
        sys.path.insert(0, dev_path)
    from mezzanine.utils.importing import path_for_import
    mezzanine_path = path_for_import("mezzanine")
    assert os.path.abspath(os.path.join(mezzanine_path, "..")) == dev_path

# Corrects some pathing issues in various contexts, such as cron jobs.
os.chdir(project_path)

for i, arg in enumerate(sys.argv):
    if arg.startswith("--site"):
        os.environ["MEZZANINE_SITE_ID"] = arg.split("=")[1]
        sys.argv.pop(i)

if __name__ == "__main__":

    DJANGO_SETTINGS_MODULE = environ['DJANGO_SETTINGS_MODULE']
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cml.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
