#!/usr/bin/make

include .env

SHELL = /bin/sh
CURRENT_UID := $(shell id -u):$(shell id -g)

export CURRENT_UID


up:
	docker-compose up -d
upb:
	docker-compose up -d --force-recreate --build
down:
	docker-compose down
prod-upb:
	docker-compose -f docker-compose-prod.yml up -d --force-recreate --build --remove-orphans
prod-down:
	docker-compose -f docker-compose-prod.yml down
sh:
	docker exec -it /birds /bin/sh
migrations:
	docker exec -it /birds python manage.py makemigrations 
	docker exec -it /birds python manage.py migrate 
