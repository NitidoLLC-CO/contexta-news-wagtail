# CONTEXTRA News Agent Notes

This project is production-first. Do not spend time preparing local browsing unless the user explicitly asks for it.

## Required Checks Before Push

Use the repository-managed environment or Docker. Do not assume the user's machine has dependencies installed.

```powershell
py -3.12 -m venv .codex-venv
.\.codex-venv\Scripts\python.exe -m pip install --upgrade pip
.\.codex-venv\Scripts\python.exe -m pip install -r requirements.txt
npm ci
npm run build:prod
$env:SECRET_KEY="codex-check-secret"
$env:DJANGO_SETTINGS_MODULE="contexta_news.settings.production"
.\.codex-venv\Scripts\python.exe manage.py check --deploy
```

For a full production image check:

```powershell
docker build -t contexta-news-wagtail .
```

## Deployment Preparation

Railway deploys from GitHub using:

- `Dockerfile`
- `railway.toml`
- `scripts/railway-start.sh`

The start script requires `DATABASE_URL`; production must use Railway PostgreSQL, not SQLite.

## Railway Required Setup

1. Create or connect the GitHub repository.
2. Create a Railway project from the GitHub repository.
3. Add a Railway PostgreSQL service.
4. Attach a Railway Volume to the web service at `/app/media`.
5. Add the environment variables documented in `README.md`.
6. Generate a Railway public domain.
7. Update `WAGTAILADMIN_BASE_URL`, `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS` with the public domain.

## Superuser

Set `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and `DJANGO_SUPERUSER_PASSWORD` in Railway to create the initial admin during deployment. Remove or rotate `DJANGO_SUPERUSER_PASSWORD` after first login.
