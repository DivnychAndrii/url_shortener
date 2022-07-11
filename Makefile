.SILENT: clear

build:
	docker-compose build

run-db: build
	docker-compose up -d postgres

run-migrations: run-db
	sleep 2 && docker-compose run server alembic -c alembic.ini upgrade heads

run: build run-migrations
	docker-compose up

run-test-db: build
	docker-compose up -d postgres-test-db

tests: run-test-db
	docker-compose run server python -m pytest --cov-config=.coveragerc --cov=source -v