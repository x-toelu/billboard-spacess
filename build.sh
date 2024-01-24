#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install -r requirements.txt

python manage.py createsuperuser --no-input --email $DJANGO_ADMIN_EMAIL

python manage.py collectstatic --no-input
python manage.py migrate