#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install -r requirements.txt

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input --email $DJANGO_ADMIN_EMAIL
fi

python manage.py collectstatic --no-input
python manage.py migrate