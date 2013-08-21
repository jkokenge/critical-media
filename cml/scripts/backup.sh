#!/bin/bash

cd /home/mel/workspace/cml/
source ../cml-env/bin/activate
gondor sqldump primary > /home/mel/Dropbox/db_backup_dropbox/critical_media_project_database.dump

