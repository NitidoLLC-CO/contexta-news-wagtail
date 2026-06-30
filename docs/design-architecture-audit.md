# Phase 1 Design Architecture Audit

CONTEXTRA News is currently a monolithic Wagtail/Django application. The same Railway web service serves the public site, Wagtail admin, Django backend, static assets, and uploaded media from the Railway volume mounted at `/app/media`.

This audit prepares for a controlled visual redesign into a premium AI intelligence news identity without changing the deployment shape.

## Page Template Structure

### Homepage

Primary files:

- `contexta_news/home/models.py`
- `templates/pages/home_page.html`
- `templates/base_page.html`
- `templates/base.html`
- `templates/components/related-pages.html`
- `templates/components/streamfield/stream_block.html`
- `templates/components/streamfield/blocks/*.html`

Model:

- `HomePage` extends `BasePage`.
- Fields: `introduction`, `hero_cta`, `body`, `featured_section_title`, related pages through `page_related_pages`.
- The homepage body is a `StoryBlock`, so most editorial body sections are rendered through StreamField block templates.

Design notes:

- The homepage hero is currently template-level markup in `templates/pages/home_page.html`.
- The global header and footer are not in the homepage template; they are injected by `templates/base_page.html`.
- Phase 2 should redesign the homepage first through `home_page.html`, `main.scss`, `tailwind.config.js`, and selected StreamField block templates.

### Article Detail Page

Primary files:

- `contexta_news/news/models.py`
- `templates/pages/article_page.html`
- `templates/components/related-pages.html`
- `templates/components/streamfield/stream_block.html`
- `templates/components/streamfield/blocks/*.html`
- `templates/navigation/breadcrumbs.html`

Model:

- `ArticlePage` extends `BasePage`.
- Parent page type: `news.NewsListingPage`.
- Fields: `author`, `topic`, `publication_date`, `introduction`, `image`, `body`, `featured_section_title`, related pages.
- `image` is a single-item `CaptionedImageBlock`.
- `body` is a `StoryBlock`.

Design notes:

- Article masthead, topic/date row, author row, lead image, and caption are all in `templates/pages/article_page.html`.
- Article body layout is mostly in StreamField block templates.
- Listing card presentation for articles is in `templates/components/card--article.html`.

### News Listing And Topic Pages

Primary files:

- `contexta_news/news/models.py`
- `templates/pages/news_listing_page.html`
- `templates/components/card--article.html`
- `templates/components/pagination.html`

Model:

- `NewsListingPage` extends `BasePage`.
- It allows only one instance through `max_count = 1`.
- It lists live `ArticlePage` children, ordered by `publication_date` or `first_published_at`.
- Topic filtering is driven by the query string: `?topic=<topic-slug>`.

Design notes:

- Category/topic pills are generated in `templates/pages/news_listing_page.html`.
- The article list uses `templates/components/card--article.html`.
- Phase 2 can create a stronger intelligence-channel layout here without model changes.

### Search

Primary files:

- `contexta_news/search/views.py`
- `templates/pages/search_view.html`
- `templates/components/card--search.html`
- `templates/components/pagination.html`
- `templates/components/search.html`
- `static_src/javascript/components/header-search-panel.js`

Behavior:

- Search uses Wagtail database search over live pages.
- Search results are rendered as page cards.
- Header search overlay is controlled by the `HeaderSearchPanel` JavaScript component.

Design notes:

- Search has its own page template plus reusable header/search component markup.
- Phase 2 should restyle search as part of the global navigation/header pass.

## Global Layout

Primary files:

- `templates/base.html`
- `templates/base_page.html`
- `templates/navigation/header.html`
- `templates/navigation/footer.html`
- `templates/navigation/breadcrumbs.html`
- `templates/components/theme-toggle.html`
- `templates/components/search.html`
- `contexta_news/navigation/models.py`

Behavior:

- `templates/base.html` defines the HTML document, metadata, CSS include, JS include, `main` landmark, and Wagtail userbar.
- `templates/base_page.html` extends `base.html`, adds favicons/theme color, and includes header/footer.
- `NavigationSettings` is a Wagtail settings model that controls primary and footer navigation via StreamFields.
- The footer also uses `SystemMessagesSettings` and `SocialMediaSettings` from `contexta_news/utils/models.py`.

Design notes:

- Header/footer should be redesigned through the existing Wagtail settings-driven navigation, not by hardcoding links.
- Keep `/admin/` paths and Wagtail userbar behavior intact.

## Styling And Asset Pipeline

### Source Files

- SCSS entry: `static_src/sass/main.scss`
- JavaScript entry: `static_src/javascript/main.js`
- JS components: `static_src/javascript/components/*.js`
- Source images/favicons: `static_src/images/**`
- Source fonts: `static_src/fonts/**`
- Compiled output: `static_compiled/**`

### Tailwind

Tailwind is active.

- Config: `tailwind.config.js`
- Dark mode: class-based, `darkMode: 'class'`
- Content scan paths:
  - `./templates/**/*.html`
  - `./static_src/**/*.{js,ts}`
- Current palette:
  - `mackerel` cyan/green-blue family
  - `grey`
  - black/white
- Current font families:
  - `sans3`
  - `serif4`
  - `codepro`

### Webpack

Config: `webpack.config.js`

Webpack:

- Entrypoint: `static_src/javascript/main.js`
- Imports `static_src/sass/main.scss`
- Outputs JS to `static_compiled/js/main.js`
- Outputs CSS to `static_compiled/css/main.css`
- Copies `static_src/images` to `static_compiled/images`
- Processes SCSS through Sass, PostCSS, Tailwind, Autoprefixer, custom properties, and cssnano.

### Package Scripts

From `package.json`:

- `npm run build` runs a development webpack build.
- `npm run build:prod` runs the production webpack build used by Docker/Railway.
- `npm start` watches source assets during local frontend development.

### Railway/Docker Build

Primary files:

- `Dockerfile`
- `railway.toml`
- `scripts/railway-start.sh`

Production build path:

1. Docker `assets` stage uses Node 22.
2. `npm ci` installs frontend dependencies.
3. `npm run build:prod` compiles frontend assets.
4. Python 3.12 production image installs Django/Wagtail requirements.
5. `collectstatic` collects `static_compiled` into `/app/static`.
6. Railway starts `scripts/railway-start.sh`.
7. Startup runs cache table creation, migrations, site configuration, superuser bootstrap if env vars are set, collectstatic, and Gunicorn on `$PORT`.

Do not split this into a separate frontend service in Phase 2.

## Wagtail Content Types

### Pages

- `HomePage` in `contexta_news/home/models.py`
- `NewsListingPage` in `contexta_news/news/models.py`
- `ArticlePage` in `contexta_news/news/models.py`
- `StandardPage` in `contexta_news/standardpages/models.py`
- `FormPage` in `contexta_news/forms/models.py`

### Snippets And Settings

- `AuthorSnippet` in `contexta_news/utils/models.py`
- `ArticleTopic` in `contexta_news/utils/models.py`
- `Statistic` in `contexta_news/utils/models.py`
- `NavigationSettings` in `contexta_news/navigation/models.py`
- `SocialMediaSettings` in `contexta_news/utils/models.py`
- `SystemMessagesSettings` in `contexta_news/utils/models.py`

### Shared Page Fields

`BasePage` in `contexta_news/utils/models.py` adds:

- social image/text fields
- listing image/title/summary fields
- search visibility toggle
- related page helpers
- plain introduction helper

## Safe Phase 2 Implementation Areas

Use these files first:

- `tailwind.config.js` for CONTEXTRA color tokens, typography tokens, shadows/glow tokens, and breakpoints if needed.
- `static_src/sass/main.scss` for global base styles, reusable component classes, body background, focus states, rich text, and layout utilities.
- `templates/base.html` for metadata, theme color, optional global body classes, and asset includes.
- `templates/base_page.html` for shared site shell behavior only.
- `templates/navigation/header.html` for premium newsroom navigation and search access.
- `templates/navigation/footer.html` for institutional footer treatment.
- `templates/pages/home_page.html` for the CONTEXTRA first-screen identity.
- `templates/pages/news_listing_page.html` for topic/channel browsing.
- `templates/pages/article_page.html` for article masthead and editorial reading experience.
- `templates/components/card--article.html`, `templates/components/card.html`, and `templates/components/card--search.html` for reusable editorial cards.
- `templates/components/streamfield/blocks/*.html` for body sections.
- `static_src/javascript/components/*.js` only where interaction changes are needed.

Avoid changing these unless required:

- `Dockerfile`
- `railway.toml`
- `scripts/railway-start.sh`
- `contexta_news/settings/production.py`
- `contexta_news/settings/base.py`
- migrations

## Risks Before Redesign

- The template is heavily utility-class driven, so visual redesign may require coordinated edits across templates and `main.scss`.
- Current palette names are template-specific (`mackerel`). Phase 2 should either map CONTEXTRA tokens onto existing names carefully or introduce new semantic tokens without breaking existing classes.
- `static_compiled/**` is committed and also generated during Docker build. After asset changes, always run `npm run build:prod` and commit the updated compiled assets.
- The mobile header currently renders primary navigation links with an empty `href`; fix this early in Phase 2.
- `static_src/javascript/main.js` initializes `ThemeToggle` twice; fix this early in Phase 2.
- Article author templates assume author images can render. If editors create authors without images, add fallbacks before the redesign depends on avatar presentation.
- Production media is currently served by Django from the Railway volume. This is acceptable for the first deployment, but high-traffic media should eventually move to object storage/CDN.
- The deployment is monolithic and should stay that way for Phase 2. Do not introduce Next.js, Vite SSR, or a separate Railway frontend service yet.
- `SECURE_SSL_REDIRECT` is enabled. Railway healthchecks use `/health/`, which is exempt; do not remove that route or change Railway healthcheck path without retesting deploys.

## Recommended Phase 2 Plan

1. Define design tokens in `tailwind.config.js`: navy/black base, electric cyan/blue accents, subdued greys, glow/shadow values, editorial typography scale.
2. Update `static_src/sass/main.scss` global base styles for the dark intelligence newsroom foundation.
3. Redesign `templates/navigation/header.html` and `templates/navigation/footer.html` first, preserving Wagtail settings-driven navigation.
4. Redesign homepage hero and first content sections in `templates/pages/home_page.html`.
5. Redesign article cards and listing pages through `card--article.html`, `card.html`, and `news_listing_page.html`.
6. Redesign `article_page.html` for high-authority editorial reading with a strong masthead, metadata, topic treatment, and clean body rhythm.
7. Audit StreamField block templates so rich article bodies match the new identity.
8. Run `npm run build:prod`, `python manage.py check --deploy`, commit compiled assets, push, and verify Railway live URLs.
9. Only after the Wagtail-rendered frontend is stable, consider optional S3/CDN media storage. Do not split the frontend service in Phase 2.
