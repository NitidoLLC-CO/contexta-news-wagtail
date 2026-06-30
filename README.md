# CONTEXTRA News

CONTEXTRA News is a Wagtail news site generated from the official Wagtail News Template:

https://github.com/wagtail/news-template

This repository is set up for a production-first Railway workflow:

1. Code is edited in this repository.
2. Changes are pushed to GitHub.
3. Railway deploys from GitHub.
4. Preview happens on the live Railway URL.

No local Python, Node, Wagtail, or PostgreSQL installation is required for production deployment.

## Runtime

- Python 3.12
- Node.js LTS for asset compilation during Docker build
- Django/Wagtail from `requirements.txt`
- PostgreSQL via Railway `DATABASE_URL`
- Gunicorn
- Whitenoise for static files
- File-system media at `/app/media` for Railway Volume first deployment

## Railway Variables

Required:

```env
DJANGO_SETTINGS_MODULE=contexta_news.settings.production
SECRET_KEY=<long-random-secret>
DATABASE_URL=${{Postgres.DATABASE_URL}}
ALLOWED_HOSTS=.up.railway.app,<your-public-domain>,healthcheck.railway.app
CSRF_TRUSTED_ORIGINS=https://*.up.railway.app,https://<your-public-domain>
WAGTAIL_SITE_NAME=CONTEXTRA News
WAGTAILADMIN_BASE_URL=https://<your-public-domain>
MEDIA_ROOT=/app/media
MEDIA_URL=/media/
SERVE_MEDIA_WITH_DJANGO=true
```

Optional first-admin variables:

```env
DJANGO_SUPERUSER_USERNAME=<admin-username>
DJANGO_SUPERUSER_EMAIL=<admin-email>
DJANGO_SUPERUSER_PASSWORD=<strong-password>
```

After the first successful login, remove `DJANGO_SUPERUSER_PASSWORD` from Railway or rotate it. To intentionally reset the admin password on deploy, add:

```env
DJANGO_SUPERUSER_RESET_PASSWORD=true
```

## Railway Media

For the first deployment, add a Railway Volume to the web service and mount it at:

```text
/app/media
```

Uploaded Wagtail images and documents are stored under `MEDIA_ROOT=/app/media`, so they survive redeploys as long as the volume remains attached. S3-compatible storage can be enabled later with the template's existing `django-storages` settings.

## Deploy Behavior

Railway uses `railway.toml` and `Dockerfile`.

On container start, `scripts/railway-start.sh` runs:

```sh
python manage.py createcachetable || true
python manage.py migrate --noinput
python manage.py configure_wagtail_site
python manage.py ensure_superuser
python manage.py collectstatic --noinput --clear
gunicorn contexta_news.wsgi:application --config gunicorn.conf.py --bind 0.0.0.0:$PORT
```

The startup script fails fast if `DATABASE_URL` is missing, so production does not silently fall back to SQLite.

## Verification Checklist

After each GitHub push and Railway deployment:

- `/health/` passes Railway healthchecks.
- Homepage loads at the Railway public URL.
- `/admin/` loads.
- Static CSS/JS loads correctly.
- Database migrations are applied.
- Admin login works.
- A test news article can be created or edited.
- Image upload works and persists after redeploy when the Railway Volume is mounted at `/app/media`.
- Mobile layout remains responsive.

## Minimal Local Developer Notes

Local development is optional. If a future developer chooses to work locally, they should use Python 3.12, Node.js LTS, and PostgreSQL or SQLite for local-only development. Production behavior is defined by the Dockerfile and Railway variables above.
