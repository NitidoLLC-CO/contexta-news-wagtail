# Phase 2I Implementation Plan

Goal: rebuild the public frontend structure for visual parity with the approved design sheets, without changing backend models, migrations, Railway, Docker, production settings, snippets, or editorial workflow fields.

## Templates To Rebuild

- `templates/navigation/header.html`
- `templates/navigation/footer.html`
- `templates/pages/home_page.html`
- `templates/pages/news_listing_page.html`
- `templates/pages/intelligence_section_page.html`
- `templates/pages/article_page.html`
- `templates/components/card--article.html`
- `templates/components/card.html`
- `templates/components/related-pages.html`

Optional only if layout breakage requires it:

- `templates/components/pagination.html`

## CSS Systems To Change

- `static_src/sass/main.scss`
- `static_compiled/css/main.css` after `npm run build:prod`

CSS work will stay inside the existing CONTEXTRA token system and add structural systems for:

- reference-like page frame
- dense hero/dashboard composition
- compact command headers
- upper dashboard band
- stronger right rails
- varied article cards
- section-specific data visuals
- app CTA/feature strip/footer density
- mobile parity ordering and spacing

No new JavaScript system is planned.

## Modules To Move

Homepage:

- Move Top Stories, AI Models Tracker, and Watchlist into a tighter upper dashboard band directly under the hero.
- Keep Live Signals attached to the hero first fold.
- Move lower modules into a compact reference-like grid: Signal Map, Trending Signals, Analysis & Insights, Research Briefs, North Signal Brief.
- Keep Footer Feature Strip and App CTA as the bottom ecosystem area.

News/section pages:

- Move featured story into the first viewport beside/under a compact command header.
- Keep live updates, signal score, trending, and section-specific modules visible earlier.
- Move lower modules into a tighter section dashboard instead of widely separated sections.

Article:

- Tighten hero, visual, context, and action bar into a more unified article briefing first fold.
- Keep Article Context and right rail modules but improve their placement and density.

## Modules To Add

Frontend-only/fallback modules where needed:

- More explicit dashboard frame panels for homepage upper band.
- Section-specific data visual variants beyond repeated North Signal watermark.
- Compact section command cards for section pages.
- Stronger right rail blocks for section/listing pages.
- Footer Feature Strip matching the reference order.
- App ecosystem CTA with phone/app fallback visual.

No new backend models will be added.

## Modules To Remove Or De-Emphasize

- De-emphasize repeated large North Signal logo visuals as generic media.
- Reduce giant intro-only section panels.
- Reduce isolated single-purpose blocks that break the reference dashboard rhythm.
- Avoid blank media areas by using existing article images or controlled visual fallbacks.

## Desktop Layout Target

Homepage:

- Header, ticker, status strip.
- Hero first fold: left editorial copy, central/right immersive visual, right Live Signals rail, micro metrics.
- Upper dashboard: Top Stories grid plus AI Models Tracker plus Watchlist.
- Lower dashboard: Signal Map, Trending Signals, Analysis & Insights, Research Briefs, North Signal Brief.
- Footer Feature Strip, North Signal App CTA, dense footer.

News listing:

- Compact command header and featured story visible quickly.
- Right rail with live updates, score/trending, and module widgets.
- Varied article feed.
- Lower document/research/analysis modules.

Section pages:

- Compact section command header with title, metrics, visual, and live updates.
- Featured story in first viewport.
- Section-specific right rail and lower modules using Phase 2G labels.
- Varied feed with no empty media.

Article:

- Article briefing shell with context rail, headline/dek/meta/actions, hero visual, and right rail.
- Readable body, pull quote, intelligence note, inline data card.
- Related stories strip.

## Mobile Layout Target

Global:

- Compact header, ticker, compact status chips, bottom nav.

Homepage:

- Hero story visible quickly.
- Live intelligence cards directly below hero.
- Top Stories with horizontal chips and compact cards.
- Lower intelligence modules stacked with strong hierarchy.

News/section:

- Compact title/summary.
- Filters/chips.
- Featured story within first viewport.
- Live updates below/near feature.
- Feed cards stacked with varied hierarchy.

Article:

- Headline and metadata early.
- Media block not oversized.
- Action chips visible.
- Context modules stacked after intro/body.
- Bottom nav does not cover content.

## Dynamic Content To Preserve

- `LiveSignal` snippets
- `StatusMetric` snippets
- `TrendingTopic` snippets
- `AIModelTrackerItem` snippets
- `MarketWatchlistItem` snippets
- `ResearchBrief` snippets
- `NorthSignalBrief` snippets
- `AppEcosystemCTA` snippets
- `ArticlePage` title, intro, body, date, author, topic, image, signal tags, workflow badges
- `IntelligenceSectionPage` labels, metrics, variants, matching articles, related snippets
- Phase 2H promotion logic for homepage/section article ordering

## Fallback Behavior To Keep

- Missing article images use controlled CONTEXTRA data visuals.
- Missing snippet data uses static fallback rows.
- Missing promoted articles fall back to latest live/public articles.
- Missing matching section articles fall back to latest live/public articles.
- Old articles without filled workflow fields continue to render.

## Implementation Sequence

1. Rebuild homepage structure and CSS for reference parity.
2. Rebuild news listing and section page structure with compact first fold and stronger rails.
3. Tighten article page structure without exposing internal notes.
4. Update shared article cards and fallback card visuals.
5. Rebuild assets.
6. Capture required desktop/mobile screenshots into `tmp/design-parity/`.
7. Write `docs/design-parity/04-final-parity-qa.md`.
8. Verify live routes, admin, static CSS, and mobile overflow.

## Non-Goals

- No backend model changes.
- No migrations.
- No new admin workflow work.
- No API ingestion.
- No Railway/Docker/production settings changes.
- No separate frontend service.
