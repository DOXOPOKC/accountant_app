#! /bin/bash

set -o errexit
set -o pipefail
cmd="$@"

function postgres_ready(){
python3 << END
import sys
import psycopg2
import environs
try:
    env = environs.Env()
    dbname = env.str('POSTGRES_DB')
    user = env.str('POSTGRES_USER')
    password = env.str('POSTGRES_PASSWORD')
    host = env.str('POSTGRES_HOST')
    port = env.str('POSTGRES_PORT')
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."

>&2 echo "Migrating..."
# python -m http.server 8000
# exec alembic upgrade head
alembic upgrade head


>&2 echo "Starting uvicorn..."
    exec uvicorn main:app --host 0.0.0.0 --port 8000"$@"