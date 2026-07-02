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
- Add section-specific visual variants if the accepted design system needs more differentiation.
