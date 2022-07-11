# URL shortener project for FoxMinded mentorship

![python 3.9](https://img.shields.io/badge/python:-3.9-yellow.svg)

# Instructions on how to run the project locally

## With Docker (recommended)

### Run

    $ make run
    
    docker alternative:
    $ docker-compose build && docker-compose up -d postgres && sleep 2 && docker-compose run server alembic -c alembic.ini upgrade heads && docker-compose up
#### Command will start the API server alongside the route with the UI page. In order to open it, navigate to:

    /home

_Note_ This will create and run containers for the server, database, and 
separate test database. It will also create a network which
all containers, which wish to speak to the server container should use.

### Run tests

    $ make tests

    docker alternative:
    $ docker-compose build && docker-compose up -d postgres-test-db && docker-compose run server python -m pytest --cov-config=.coveragerc --cov=source -v
_None_ It will create a test database instance in a container and run tests using it. Coverage will be shown after


## Without Docker

_Note_ On some machines you might need to install python 3.9 and 
postgres installed, you might need to install first.

### Install dependencies

    $ pipenv sync

_Note_ On some machines you will be needed to install to ensure that psycopg2 module works correctly.
If you get any troubles installing psycopg2 library from dependencies, run next command:

    $ apt-get update && apt-get install gcc libpq-dev -y

### Run local dev server
    
    $ python3 main.py

### For proper local set up you will need a postgres database
To ensure that your server can use your local database, please run:
    
    $ export SQLALCHEMY_DATABASE_URI='postgresql://postgres@postgres:5432/postgres?sslmode=disable'

_Note_ Use your local database URI.

To ensure your local database has a proper structure of the tables, please run migrations:
    
    $ export SQLALCHEMY_DATABASE_URI='postgresql://postgres@postgres:5432/postgres?sslmode=disable'
    $ alembic upgrade head

