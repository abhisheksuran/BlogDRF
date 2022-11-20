# Blog Rest API

## Description:

A simple Blog Rest API based on Django-Rest-Framework. 
Swagger docs can be access at http://localhost:8000/api/docs/

## For Development SetUp

Run following commands for setting up development environment.

1. docker-compose build
2. docker-compose up

## For running custom command:

docker-compose run --rm app sh -c "YOUR COMMAND"

example: docker-compose run --rm app sh -c "python manage.py shell"

## For Deployment:

1. sudo docker-compose -f docker-compose-deploy.yml build
2. sudo docker-compose -f docker-compose-deploy.yml up


