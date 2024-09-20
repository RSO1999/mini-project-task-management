#!/bin/bash

#FRESH DATABASE 
echo "spinning a fresh database up" 
docker-compose up database -d --remove-orphans

echo "sleeping 5 seconds to let the database start up"
sleep 5

#APPLY MIGRATIONS
echo "applying schema migrations"
docker-compose run django python manage.py makemigrations
docker-compose run django python manage.py migrate

#START DJANGO APP
echo "starting django app"
docker-compose up django -d --remove-orphans

#DISPLAY CONTAINERS
echo "CONTAINER STATUSES"
docker ps