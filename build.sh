#!/usr/bin/env bash 
#exit o error 
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate 
python manage.py superuser