#!/bin/bash

date
python manage.py migrate
python manage.py crontab add .
python manage.py crontab show
service cron start
service cron status

python manage.py runserver 0.0.0.0:8000