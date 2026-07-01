# CONTEXTRA Intelligence Admin Modules

Phase 2D adds Wagtail-admin-managed snippets for the intelligence widgets used by the accepted public frontend. The visual system is unchanged; templates now prefer active snippet data and keep the previous static fallback content when no snippet data exists.

## New Wagtail Snippets

- `LiveSignal`: powers the global ticker, homepage Live Signals, `/news/` Live Updates, and article Related Signals.
- `StatusMetric`: powers the global North Signal status strip and `/news/` section metrics.
- `TrendingTopic`: powers homepage Trending Signals and `/news/` Trending Topics.
- `AIModelTrackerItem`: powers the homepage AI Models Tracker.
- `MarketWatchlistItem`: powers the homepage Watchlist and article Market Snapshot.
- `ResearchBrief`: powers homepage Research Briefs and `/news/` Policy Documents & Research.
- `NorthSignalBrief`: powers the homepage North Signal Brief and `/news/` mini brief module.
- `AppEcosystemCTA`: powers the footer/bottom North Signal app CTA.

## Files Added

- `contexta_news/intelligence/models.py`
- `contexta_news/intelligence/migrations/0001_initial.py`
- `contexta_news/intelligence/templatetags/intelligence_tags.py`
- `contexta_news/intelligence/management/commands/seed_contextra_intelligence.py`

## Template Connections

- `templates/navigation/header.html`
  - Uses active `LiveSignal` rows for the ticker.
  - Uses active `StatusMetric` rows for the status strip.
- `templates/pages/home_page.html`
  - Uses snippets for Live Signals, AI Models Tracker, Watchlist, Trending Signals, Research Briefs, and North Signal Brief.
  - Keeps Wagtail article-driven lead/top stories unchanged.
- `templates/pages/news_listing_page.html`
  - Uses snippets for Live Updates, section metrics, Trending Topics, Research/Documents, and North Signal Brief.
  - Keeps Wagtail article listing, filtering, featured story, and pagination unchanged.
- `templates/pages/article_page.html`
  - Uses snippets for Related Signals and Market Snapshot.
  - Keeps article body, author, topic, title, dek, image, and related pages unchanged.
- `templates/navigation/footer.html`
  - Uses `AppEcosystemCTA` for the bottom app/ecosystem CTA.

## Fallback Behavior

Every connected template keeps a static fallback branch. If snippets are empty or inactive, the public frontend still renders the accepted Phase 2 public design instead of empty panels.

## Seed Data

Run:

```powershell
python manage.py seed_contextra_intelligence
```

The command is idempotent. It creates the initial sample records only if each snippet table is empty, then no-ops on later runs.

Seeded examples include:

- OpenAI expands model context window to 2M tokens
- EU AI Act implementation guidelines published
- Global GPU supply tightens as demand accelerates
- North Signal Status Active
- Systems Monitoring 98.7%
- Signals Today 1,248
- Market Sentiment Bullish
- AI model tracker rows
- Watchlist tickers
- Research briefs
- North Signal Brief
- North Signal app CTA

## Phase 2E Notes

- Add editorial grouping or placement controls if editors need multiple homepage variants.
- Add newsletter capture handling before making the North Signal form submit real subscriptions.
- Add richer per-article intelligence fields if Article Intelligence score, Key Takeaways, and Article Context need to become editorial data.
- Consider API-backed market/model data once the editorial workflow is stable.
