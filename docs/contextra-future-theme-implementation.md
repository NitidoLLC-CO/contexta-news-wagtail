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

## Phase 2A.1 Polish

Phase 2A.1 corrects the homepage hero and mobile hierarchy without starting Phase 2B.

Changes:

- Replaced the plain radar/grid hero fallback with a reusable CONTEXTRA signal visual system.
- Added `contextra-signal-visual`, `contextra-hologram-core`, `contextra-orbit-lines`, `contextra-data-grid`, signal streams, map nodes, and micro-panels.
- Kept Wagtail article images available, but layered the holographic system over/behind them so weak placeholder images do not create blank panels.
- Improved the Latest Signals rail with stronger glass panels, impact badges, timestamps, and hover depth.
- Fixed mobile hero order so the visual no longer appears as a large block before the headline.
- On mobile, the hero visual becomes a compact atmospheric background behind the editorial card content.

Still unchanged:

- Wagtail models and migrations
- Article detail template
- News listing template
- Railway, Docker, database, production, and media settings

## Phase 2B Article Detail

Phase 2B rebuilds the article detail page into a CONTEXTRA intelligence briefing while preserving the existing Wagtail article model, publishing flow, media handling, and Railway deployment.

Changed:

- `templates/pages/article_page.html`
- `static_src/sass/main.scss`
- `static_compiled/css/main.css` after the production frontend build

Dynamic article mapping:

- `page.title` renders as the article headline.
- `page.introduction` or `page.search_description` renders as the dek.
- `page.display_date` renders in the briefing metadata.
- `page.author.title` renders in the byline and author module when present.
- `page.topic` renders in article signal tags and related topic chips.
- `page.image` renders inside the premium hero visual when available.
- `page.body` remains the source of the article body through Wagtail rich text / StreamField rendering.
- `page.related_pages` continues to feed the related intelligence strip.

Static Phase 2B fallback modules:

- Signal tags such as High Impact, AI Infrastructure, and Market Signal.
- Listen, Share, Save, Cite, and Print action chips.
- Article Context, Key Takeaways, Related Topics, Article Intelligence score, Related Signals, and Signal Intelligence card.
- These are intentionally isolated in `templates/pages/article_page.html` so they can become Wagtail snippets, editorial fields, or API-backed modules later.

Responsive article behavior:

- Desktop uses a three-column intelligence layout with context rail, readable body, and signal modules.
- Tablet moves the context rail above the main article and keeps the side intelligence rail beside the body where space allows.
- Mobile stacks all article modules, keeps the headline early, caps the hero visual height, and allows action chips to scroll horizontally.

Phase 2C recommendations:

- Rebuild listing and section pages into the same future-newsroom language.
- Replace static article intelligence modules with Wagtail-managed fields/snippets.
- Add real share/listen/save behavior if those become active product features.
- Add curated related-signal logic beyond the existing related pages relation.

## Phase 2C Section / Listing Pages

Phase 2C rebuilds `/news/` and topic-filtered listing views into a CONTEXTRA Intelligence Feed section hub while preserving the existing Wagtail listing page model, article children, pagination, topic query links, and Railway deployment.

Changed:

- `templates/pages/news_listing_page.html`
- `templates/components/card--article.html`
- `static_src/sass/main.scss`
- `static_compiled/css/main.css` after the production frontend build

Dynamic listing mapping:

- `page.title` renders as the section headline.
- `page.introduction` or `page.search_description` renders as the section dek.
- `topics` and `matching_topic` continue to support topic query links.
- The first item in `paginator_page.object_list` renders as the featured lead story.
- Remaining child `ArticlePage` items render into the main feed grid.
- Article cards use Wagtail title/listing title, listing summary/introduction, topic, date, author, and listing image.
- Existing pagination remains active through `components/pagination.html`.

Static Phase 2C fallback modules:

- Section signal metrics.
- Required visual topic chips for All, AI, Technology, Companies, Policy, Markets, Research, and Infrastructure.
- Signal Score, Trending Topics, Market Snapshot, North Signal Brief, Research & Documents, Analysis & Insights, and Global Signal Map.
- These are isolated in `templates/pages/news_listing_page.html` for later conversion to snippets, editorial fields, or API-backed modules.

Responsive section behavior:

- Desktop uses a section hero, featured story, dynamic article feed, sticky intelligence rail, and lower intelligence modules.
- Tablet stacks the hero visual and featured media while preserving a structured feed.
- Mobile hides the decorative section visual, keeps the title and featured story early, scrolls topic chips horizontally, stacks feed cards and right rail modules, and avoids oversized empty panels.

Phase 2D recommendations:

- Convert static section modules into Wagtail snippets or API-backed widgets.
- Add real backend filtering for the fixed topic chips where matching Wagtail topics do not yet exist.
- Revisit search results and other utility pages so the full public site shares the same future-newsroom language.

## Design War Room Rebuild

The rejected Phase 2C was replaced with a supervised design war-room sprint focused on closing the gap with the approved reference images in `contexctra branding/`.

Changed direction:

- Replaced incremental listing-page polish with a broader public frontend rebuild.
- Added design war-room audit/planning documents under `docs/design-war-room/`.
- Added optimized web-ready North Signal brand assets derived from the approved branding images.
- Reworked global header/footer/mobile shell to use the real brand asset instead of only the CSS-drawn mark.
- Added safe-area-aware mobile bottom navigation.
- Strengthened homepage first fold with lead metrics and real brand watermark.
- Rebuilt `/news/` into a section command center with section hero, metrics, filters, live updates, featured story, signal score, trackers, video brief, research/documents, analysis, expert/event modules, and dynamic feed rhythm.
- Refined article page with brand watermark, share/print affordances, and market snapshot rail while preserving Wagtail body rendering.
- Upgraded shared article cards with branded fallback media and richer variants.

Dynamic Wagtail content remains:

- homepage lead story, latest signals, and top stories
- listing featured story and paginated article feed
- article title, dek, body, topic, author, date, image, and related pages

Static fallback modules remain:

- ticker/status metrics
- model tracker
- watchlist
- signal map
- trending signals/topics
- trackers
- video brief
- market snapshot
- research/document rows
- North Signal Brief
- app CTA

Remaining limitations:

- Static intelligence widgets should become Wagtail snippets or API-backed modules later.
- Fixed topic links may not match all Wagtail topic slugs until taxonomy is expanded.
- Search, standard pages, forms, and streamfield utility blocks still need a dedicated cleanup pass.

## Phase 2D Intelligence Admin Modules

Phase 2D converts the accepted static intelligence widgets into Wagtail-admin-managed snippets while preserving the current public visual system and monolithic Railway deployment.

New dynamic snippet-backed modules:

- Global ticker: `LiveSignal`
- Global status strip: `StatusMetric`
- Homepage Live Signals: `LiveSignal`
- Homepage AI Models Tracker: `AIModelTrackerItem`
- Homepage Watchlist: `MarketWatchlistItem`
- Homepage Trending Signals: `TrendingTopic`
- Homepage Research Briefs: `ResearchBrief`
- Homepage North Signal Brief: `NorthSignalBrief`
- `/news/` Live Updates: `LiveSignal`
- `/news/` section metrics: `StatusMetric`
- `/news/` Trending Topics: `TrendingTopic`
- `/news/` Research/Documents: `ResearchBrief`
- `/news/` North Signal mini brief: `NorthSignalBrief`
- Article Market Snapshot: `MarketWatchlistItem`
- Article Related Signals: `LiveSignal`
- Footer App/Ecosystem CTA: `AppEcosystemCTA`

Static fallback branches remain in every connected template so the site does not go empty if snippet records are disabled or not seeded.

Operational notes:

- Migration: `contexta_news/intelligence/migrations/0001_initial.py`
- Seed command: `python manage.py seed_contextra_intelligence`
- Documentation: `docs/contextra-intelligence-admin-modules.md`
