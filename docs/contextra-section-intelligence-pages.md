# CONTEXTRA Section Intelligence Pages

Phase 2F adds real Wagtail-managed topic/section pages for the main CONTEXTRA navigation. The accepted homepage, `/news/`, article template, Phase 2D snippets, and Phase 2E article intelligence workflow remain intact.

## Approach Chosen

The project now uses a new Wagtail page model:

- `IntelligenceSectionPage`

This model lives in `contexta_news.news.models` because it is part of the editorial/news content architecture and needs to query `ArticlePage` directly.

Seeded public section URLs:

- `/ai/`
- `/technology/`
- `/companies/`
- `/policy/`
- `/markets/`
- `/research/`

The existing `/news/` listing page remains unchanged and continues to serve the global feed.

## Admin Workflow

Editors can manage each section page in Wagtail like any other page. The section editor supports:

- section name
- section label
- subtitle/dek
- visual mode
- comma-separated article matching terms
- optional featured article
- optional section signal score
- optional CTA label and URL
- ordered section metrics
- curated Live Signal snippets
- curated Trending Topic snippets
- curated Research Brief snippets
- curated Market/Watchlist snippets

If curated snippet rows are empty, the frontend uses active Phase 2D snippets as fallback.

## Navigation Behavior

The global header and footer now link to the real section pages:

- AI -> `/ai/`
- Technology -> `/technology/`
- Companies -> `/companies/`
- Policy -> `/policy/`
- Markets -> `/markets/`
- Research -> `/research/`

The mobile navigation and mobile bottom Watchlist link were updated as well.

## Article Matching Logic

Each `IntelligenceSectionPage` has `matching_terms`. The section query checks those terms against:

- article topic slug
- article topic title
- article context label
- article title
- article introduction
- article signal tags

If no article matches, the section falls back to the latest published articles so the page never appears empty.

## Seed Command

Run:

```powershell
python manage.py seed_contextra_sections
```

The command creates or updates the six section pages and publishes them. It is idempotent:

- first run creates the pages
- later runs update metadata without creating duplicates

The command also attaches default metrics and available Phase 2D snippets to each section where present.

## Fallback Behavior

Fallbacks are intentionally layered:

- no matching articles -> latest published articles
- no curated Live Signals -> active LiveSignal snippets
- no curated Trending Topics -> active TrendingTopic snippets
- no curated Research Briefs -> active ResearchBrief snippets
- no curated Watchlist Items -> active MarketWatchlistItem snippets
- no snippets at all -> controlled static fallback rows

## Future Improvements

- Add per-section editorial card ordering.
- Add stronger topic taxonomy and article-to-section relations.
- Add section-specific analysis modules.
- Add API-backed market/model/research feeds after editorial workflow stabilizes.
- Add deeper section-specific imagery if the accepted design system needs more differentiation.

## Phase 2G Section-Specific Intelligence Variants

Phase 2G keeps the same `IntelligenceSectionPage` model fields and does not add a migration. The existing `visual_mode`, labels, metrics, matching terms, snippets, CTA, and featured article fields are enough for the first section-specific variant layer.

Implemented variants:

- AI: model signals, agentic watch, benchmark drift, frontier models, agent infrastructure, safety signals.
- Technology: infrastructure updates, chip signals, cloud capacity, semiconductor watch, cloud buildout, systems briefs.
- Companies: strategic moves, funding signals, model-provider watch, deals, partnerships, product launches.
- Policy: regulation watch, export controls, sovereignty signals, government actions, safety institutes, public investment.
- Markets: capex signals, AI infrastructure index, stock watch, market snapshot, valuation pressure, spending trends.
- Research: paper signals, benchmark watch, evaluation notes, research briefs, model evaluations, safety findings.

Template behavior:

- `templates/pages/intelligence_section_page.html` reads `section_variant` from the page context.
- Each variant changes hero visual label, right-rail headings, score copy, feed headings, watchlist headings, research headings, analysis headings, lower signal modules, and static fallback rows.
- The page still uses the accepted CONTEXTRA shell, ticker, status strip, glass panels, North Signal identity, article feed, snippets, and fallback safeguards.

Seed behavior:

- `seed_contextra_sections` remains idempotent.
- Repeated runs update the six section pages, publish revisions, refresh default metrics, and refresh default related snippet rows without creating duplicates.
- The command now attempts to match articles and snippets against each section's expanded matching terms before using static variant fallbacks in the template.

No new model fields were added in Phase 2G.
