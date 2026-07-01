# Design War Room Final QA Report

Date: 2026-07-01

## Scope

Final QA pass for the supervised design war room rebuild of the public CONTEXTRA News frontend. The Wagtail backend, admin, models, database, media settings, Dockerfile, Railway configuration, and production settings were intentionally left unchanged.

## Local Build And Django Checks

- `npm run build:prod`: passed.
- `DJANGO_SETTINGS_MODULE=contexta_news.settings.production python manage.py check --deploy`: passed with a strong temporary check `SECRET_KEY`.
- Mojibake scan across `templates`, `static_src`, and `docs`: passed.
- Migration check from the implementation pass: no model changes detected.

## Live Route Checks

Checked against `https://contexta-news-wagtail-production.up.railway.app`.

- `/`: HTTP 200.
- `/news/`: HTTP 200.
- `/news/deployment-test-article/`: HTTP 200.
- `/admin/`: HTTP 200 after following the login redirect.
- Homepage references compiled `/static/css/main.*.css`.
- North Signal compiled image asset `/static/images/contextra/north-signal-mark-small.webp`: HTTP 200.

## Screenshot Evidence

Browser capture in this Windows session was unstable:

- The in-app browser successfully captured desktop homepage and desktop news listing screenshots.
- The in-app browser timed out when capturing additional article/mobile screenshots.
- System Chrome, Edge, and Playwright-managed Chromium all launched and immediately exited before screenshots could be produced.
- Public screenshot services returned blank or placeholder images and were not accepted as QA evidence.

Available screenshot artifacts:

- `tmp/war-room-home-desktop.png`
- `tmp/war-room-news-desktop.png`

The desktop homepage screenshot exposed a real visual issue: the lead headline could run under the hero visual column at desktop width. That issue was fixed by constraining `.cx-lead-system__content`, reducing the lead headline desktop clamp, setting headline letter spacing to `0`, and allowing safe word wrapping.

## QA Verdict

Superseded by `06-qa-lockdown-audit.md`.

This QA verdict is invalid because it accepted the redesign without all six required desktop/mobile screenshots. The route checks and build checks were useful, but they were not enough for visual-design acceptance.

## Remaining Risks Before The Next Phase

- Full desktop/mobile screenshot capture should be repeated from a stable browser environment after Railway redeploy.
- Some old template utility CSS still exists because the rebuild intentionally avoided backend/model churn.
- Listing and article pages now follow the future-newsroom system, but Phase 2D should refine deeper article body modules and real dynamic sources for static intelligence widgets.
