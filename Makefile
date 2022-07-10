.SILENT: clear

build:
	docker-compose build
run:
	docker-compose up

run-test-db:
	docker-compose up -d postgres-test-db

tests: build run-test-db
	docker-compose run server python -m pytest --cov-config=.coveragerc --cov=source -v