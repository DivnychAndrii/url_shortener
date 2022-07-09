# URL shortener project for FoxMinded mentorship

![python 3.9](https://img.shields.io/badge/python:-3.9-yellow.svg)

# Instructions on how to run the project locally

## With Docker (recommended)

### Run

    $ make run.local

_Note_ This will create and run containers for the server, database, and 
separate test database. It will also create a network which
all containers, which wish to speak to the server container should use.


## Without Docker

_Note_ On some machines you might need to install python 3.9 and 
postgres installed, you might need to install first.

### Install dependencies

    $ pipenv sync -d

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

