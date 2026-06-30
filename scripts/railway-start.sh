#!/bin/sh
set -eu

: "${DATABASE_URL:?DATABASE_URL must be set by the Railway PostgreSQL service.}"

python manage.py createcachetable || true
python manage.py migrate --noinput
python manage.py configure_wagtail_site
python manage.py ensure_superuser
python manage.py collectstatic --noinput --clear

exec gunicorn contexta_news.wsgi:application \
    --config gunicorn.conf.py \
    --bind "0.0.0.0:${PORT:-8000}"
