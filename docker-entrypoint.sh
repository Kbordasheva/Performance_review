#!/bin/bash

# Get DB credentials from the environment and try to connect to Postgres
function postgres_ready() {
  python <<END
import sys
import psycopg2
from os import environ

try:
    conn = psycopg2.connect(dbname=environ.get("DATABASE_NAME"), user=environ.get("DATABASE_USER"),
                            password=environ.get("DATABASE_PASSWORD"), host=environ.get("DATABASE_HOST"),
                            port=environ.get("DATABASE_PORT"))
except psycopg2.OperationalError as e:
    print(e)
    sys.exit(-1)
sys.exit(0)
END
}

source /venv/bin/activate

# Do not execute next code until postgres is up and running
until postgres_ready; do
  echo >&2 "Postgres is unavailable - sleeping"
  sleep 1
done

# Migrate if any new migrations present and collect static
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# Run gunicorn with 8 workers
gunicorn src.wsgi:application --workers=8 --bind 0.0.0.0:8001 \
  --access-logfile access.log --error-logfile error.log \
  --log-level=debug --capture-output