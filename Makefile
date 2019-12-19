#!/usr/bin/make

include .env

SHELL = /bin/sh
CURRENT_UID := $(shell id -u):$(shell id -g)

export CURRENT_UID

MSG := ""

up:
	docker-compose up -d
upb:
	docker-compose up -d --force-recreate --build
down:
	docker-compose down
sh:
	docker exec -it /FastAPI /bin/sh
migrations:
	docker exec -it /FastAPI alembic revision --autogenerate -m "$(MSG)"
