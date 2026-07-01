# 00 Super Agent Plan

## Decision

The rejected Phase 2C will be replaced by a controlled public theme rebuild sprint. This is still frontend-only inside the monolithic Wagtail/Django service.

No Wagtail models, migrations, Railway settings, Dockerfile, production settings, database settings, or media settings will be changed.

## Exact Pages To Rebuild

1. Global shell/header/footer.
2. Homepage.
3. `/news/` listing / section hub.
4. Article detail consistency pass.
5. Mobile shell and responsive behavior across the above.

## Exact Files To Change

Planned code files:

- `templates/navigation/header.html`
- `templates/navigation/footer.html`
- `templates/pages/home_page.html`
- `templates/pages/news_listing_page.html`
- `templates/pages/article_page.html`
- `templates/components/card--article.html`
- `templates/components/card.html`
- `templates/components/related-pages.html`
- `templates/components/pagination.html`
- `static_src/sass/main.scss`
- `static_compiled/css/main.css`
- `docs/contextra-future-theme-implementation.md`
- `docs/design-war-room/*.md`

Asset files may be added only as optimized web-ready derivatives of approved branding images so the public shell can use the real CONTEXTRA/North Signal identity.

## Reference Elements To Implement

- Real CONTEXTRA/North Signal mark in header/footer/mobile.
- Compact top shell, live ticker, and status metric strip.
- Dense homepage first fold with lead story, cinematic visual, latest signals, and visible next section.
- Top stories row with varied card rhythm.
- AI Models Tracker, Watchlist, Signal Map, Trending Signals, Analysis, Research Briefs, North Signal Brief, app CTA.
- `/news/` as a section command center with filters, featured story, live updates, score, trackers, research, analysis/video, expert perspective, and CTA.
- Article detail as a premium intelligence briefing with readable body and denser supporting rails.
- Mobile bottom navigation and app-like stacked feed behavior.

## Static Fallbacks

The following stay static in this sprint:

- ticker items
- status metrics
- model tracker
- watchlist
- market snapshot
- trending signals
- research/doc rows
- North Signal Brief
- app CTA
- article signal score/takeaways where no model exists

They must look intentional and isolated for later conversion to Wagtail snippets/API-backed widgets.

## Mobile Rules

- Keep brand mark visible.
- No huge empty visuals before useful content.
- Metrics and chips may scroll horizontally.
- Story cards stack cleanly.
- Rails move below primary content.
- Bottom nav must not cover content; add safe-area/body bottom padding.
- Article body remains readable.

## QA Acceptance Criteria

Desktop:

- Homepage no longer reads as a generic dark template.
- `/news/` reads as a real section/intelligence hub.
- Article page remains readable and visually consistent.
- No large blank media panels.
- Cards have varied hierarchy.
- Real brand assets appear in shell/footer/CTA.

Mobile:

- First viewport is useful and branded.
- Bottom nav is usable and does not cover content.
- Listing page shows useful content quickly.
- No accidental horizontal overflow except chip/metric/action scrollers.

Technical:

- `npm run build:prod` passes.
- `manage.py check --deploy` passes.
- Live `/`, `/news/`, `/news/deployment-test-article/`, `/admin/`, and static CSS verify after Railway deploy.

## Implementation Approval

Approved to implement the sprint after this plan. The implementation must be broad enough to close the visual gap and not limited to isolated CSS tweaks.
