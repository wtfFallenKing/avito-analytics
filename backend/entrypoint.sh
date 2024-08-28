#!/bin/bash


echo "Migrate the database at startup of project"

while ! alembic upgrade head  2>&1; do
  echo "Migration is in progress status"
  sleep 3
done

echo "Migration done"

exec python3 main.py
