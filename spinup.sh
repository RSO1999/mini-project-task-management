#!/bin/bash

#FRESH DATABASE 
echo "spinning a fresh database up" 
docker-compose up database -d --remove-orphans

echo "sleeping 5 seconds to let the database start up"
sleep 5

#APPLY MIGRATIONS
echo "applying schema migrations"


#START DJANGO APP
echo "starting django app"
docker-compose up django --build -d --remove-orphans

#DISPLAY CONTAINERS
echo "CONTAINER STATUSES"
docker ps