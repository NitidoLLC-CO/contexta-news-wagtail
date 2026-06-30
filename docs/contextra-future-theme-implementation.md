# CONTEXTRA Future Theme Implementation

## Phase 2A Scope

Phase 2A implements the CONTEXTRA future homepage and global public shell inside the existing monolithic Wagtail/Django project. Wagtail remains responsible for admin, users, publishing, pages, articles, images, media, and PostgreSQL-backed content.

No model, migration, database, Docker, Railway, production settings, or media settings changes were made.

## Templates Changed

- `templates/navigation/header.html`
- `templates/navigation/footer.html`
- `templates/pages/home_page.html`
- `templates/components/card--article.html`
- `templates/components/card.html`

## Styling Changed

- `static_src/sass/main.scss`
- `static_compiled/css/main.css` after the production frontend build

## Dynamic Homepage Mapping

- Lead story uses the latest live Wagtail `ArticlePage` provided by `HomePage.get_context`.
- Top Stories uses the latest available Wagtail articles.
- Live Signals uses available recent Wagtail articles when present.
- Article cards use Wagtail title, listing title, listing summary, introduction fallback, topic, display date, author, and listing image.
- If an article has no listing image, the frontend renders a controlled CONTEXTRA signal-panel fallback instead of a broken image.

## Static Fallback Modules

These sections are intentionally static in Phase 2A and isolated in `templates/pages/home_page.html` so they can be connected to real models or APIs later:

- AI Models Tracker
- Watchlist
- Signal Map
- Trending Signals
- Analysis & Insights
- Research Briefs
- North Signal Brief
- North Signal App / ecosystem CTA
- Header live ticker and North Signal status strip

## Responsive Behavior

- Desktop uses a dense intelligence-newsroom grid with a hero lead story, live signals sidebar, top stories row, and modular data panels.
- Tablet collapses the hero/sidebar and intelligence panels into two-column layouts.
- Mobile stacks the hero, signal panel, top stories, and modules into a single-column experience.
- Header navigation becomes a compact details-based menu without adding JavaScript.
- Ticker, metrics, and filter chips use horizontal overflow on small screens.

## Phase 2B Recommendations

- Rebuild section/listing pages into the Policy & Power style reference.
- Rebuild article detail pages with context rail, action bar, market snapshot, related signals, and article intelligence modules.
- Replace static fallback widgets with Wagtail snippets or API-backed data sources.
- Add real newsletter capture handling if North Signal Brief becomes active.
- Consider adding curated homepage slots instead of relying only on latest articles.
