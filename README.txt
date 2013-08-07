to run:

source ../cml-env/bin/activate
python manage.py runserver --settings=cml.dev_settings


to deploy:

gondor env:set primary DJANGO_SETTINGS_MODULE=cml.settings
gondor deploy primary default