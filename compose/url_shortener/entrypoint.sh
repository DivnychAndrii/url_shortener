#!/bin/bash
# set -e

function db_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect("$SQLALCHEMY_DATABASE_URI")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until db_ready; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - continuing"
>&2 echo "Running migration"

alembic upgrade head &&

exec "$@"


