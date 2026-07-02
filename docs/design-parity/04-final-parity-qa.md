# Phase 2I Final Parity QA

Date: 2026-07-02

Live URL: https://contexta-news-wagtail-production.up.railway.app/

Railway deployment verified: `fd361c80-5894-4f90-9eea-ad2480c542e0` reached `SUCCESS` after pushing commit `79c3f84`.

## Screenshot Evidence

Screenshots were captured from the live Railway deployment into `tmp/design-parity/`.

Required set:

- `tmp/design-parity/home-desktop.png`
- `tmp/design-parity/home-mobile.png`
- `tmp/design-parity/news-desktop.png`
- `tmp/design-parity/news-mobile.png`
- `tmp/design-parity/ai-desktop.png`
- `tmp/design-parity/ai-mobile.png`
- `tmp/design-parity/policy-desktop.png`
- `tmp/design-parity/policy-mobile.png`
- `tmp/design-parity/markets-desktop.png`
- `tmp/design-parity/markets-mobile.png`
- `tmp/design-parity/research-desktop.png`
- `tmp/design-parity/research-mobile.png`
- `tmp/design-parity/article-desktop.png`
- `tmp/design-parity/article-mobile.png`

Additional section coverage:

- `tmp/design-parity/technology-desktop.png`
- `tmp/design-parity/technology-mobile.png`
- `tmp/design-parity/companies-desktop.png`
- `tmp/design-parity/companies-mobile.png`

## Route Verification

Live route checks:

- `/` returned `200`
- `/news/` returned `200`
- `/ai/` returned `200`
- `/technology/` returned `200`
- `/companies/` returned `200`
- `/policy/` returned `200`
- `/markets/` returned `200`
- `/research/` returned `200`
- `/news/deployment-test-article/` returned `200`
- `/static/css/main.css` returned `200`
- `/admin/` returned `302` to `/admin/login/?next=/admin/`
- `/admin/login/?next=/admin/` returned `200`

Browser checks on the captured pages confirmed CSS was loaded and no horizontal overflow was detected at desktop or mobile viewport sizes.

## What Now Matches The Reference Direction

- Homepage first fold now behaves like a dense intelligence command center rather than a simple hero plus blog grid.
- Lead story, Live Signals, Top Stories, AI Models Tracker, and Watchlist sit in a tighter upper dashboard band.
- Lower homepage modules now form a compact dashboard strip: Signal Map, Trending Signals, Analysis, Research Briefs, and North Signal Brief.
- Section pages use compact first folds with title, metrics, visual module, live rail, chip dock, and featured story visible earlier.
- Article page first fold is tighter and more briefing-like, with metadata, signal tags, action chips, hero visual, and context modules visible sooner.
- Repeated missing-image placeholders now use controlled data visuals instead of only repeating the North Signal logo.
- Mobile pages show the headline/section title quickly, keep the ticker/status language, preserve bottom navigation, and avoid horizontal overflow.

## Dynamic Modules Preserved

- Live signal snippets
- Status metric snippets
- Trending topic snippets
- AI model tracker snippets
- Market watchlist snippets
- Research brief snippets
- North Signal brief snippet
- App ecosystem CTA snippet
- Article title, intro, body, author, date, topic, image, signal tags, workflow badges, and intelligence fields
- Section page variants, metrics, matching articles, related snippets, and fallback article logic

## Remaining Differences

- The reference image has more bespoke visual assets and deeper variation per module. Phase 2I uses CSS-driven data visuals and existing brand assets to avoid adding new architecture or media dependencies.
- Section pages still share the same base layout pattern, with variant copy and glyph treatments creating the distinction. More bespoke per-section modules can be added later.
- Some right-rail content is intentionally clipped by the first viewport on desktop because the layout is dense and app-like; the live pages do not horizontally overflow.
- Mobile bottom navigation is fixed and can cover the very bottom edge of long modules, but content remains scrollable and the first viewport is usable.

## QA Verdict

Phase 2I is ready for review as the public frontend design-sheet parity rebuild. The implementation is live, screenshots exist, public routes load, admin remains protected, static CSS loads, and no model, migration, Railway, Docker, or production settings changes were made.
