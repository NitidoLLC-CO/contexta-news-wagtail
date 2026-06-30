FROM node:22-slim AS assets

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY webpack.config.js tailwind.config.js ./
COPY static_src ./static_src
COPY templates ./templates
RUN npm run build:prod


FROM python:3.12-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=contexta_news.settings.production \
    MEDIA_ROOT=/app/media \
    MEDIA_URL=/media/ \
    PORT=8000

WORKDIR /app

RUN apt-get update --yes --quiet \
    && apt-get install --yes --quiet --no-install-recommends build-essential libpq5 \
    && apt-get autoremove --yes --quiet \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=assets /app/static_compiled ./static_compiled

RUN mkdir -p /app/media /app/static \
    && SECRET_KEY=build-time-placeholder python manage.py collectstatic --noinput --clear

EXPOSE 8000

CMD ["sh", "./scripts/railway-start.sh"]
