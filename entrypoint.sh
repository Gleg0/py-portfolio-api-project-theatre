#!/bin/sh

echo "Waiting for database..."
python manage.py wait_for_db

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn cinema_service.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
