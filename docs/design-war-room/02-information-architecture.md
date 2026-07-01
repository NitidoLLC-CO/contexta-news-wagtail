# 02 Information Architecture

## Platform Model

CONTEXTRA should behave like a live intelligence-news platform. Public pages should organize content as signals, briefings, trackers, research, and contextual intelligence rather than as a normal blog archive.

## Global Page Order

1. Brand shell
2. Primary navigation
3. Intelligence search entry
4. Live Signal Ticker
5. North Signal status metrics
6. Page-specific command surface
7. Dynamic editorial content
8. Static fallback intelligence widgets
9. Platform trust strip
10. North Signal app / ecosystem CTA
11. Footer
12. Mobile bottom nav on small screens

## Homepage IA

Desktop first fold must contain:

- CONTEXTRA brand shell
- Live Signal Ticker
- North Signal status metrics
- Lead story text
- Immersive media / North Signal visual
- Latest Signals rail
- Hint of Top Stories below

Homepage modules:

1. Lead Story System: latest Wagtail article where available.
2. Live Signals Rail: next newest articles or static fallback signals.
3. Top Stories: dynamic articles with varied cards.
4. AI Models Tracker: static fallback.
5. Watchlist: static fallback.
6. Signal Map: CSS/brand visual, never blank.
7. Trending Signals: static fallback.
8. Analysis & Insights: static fallback or dynamic article later.
9. Research Briefs: static fallback.
10. North Signal Brief: static CTA.
11. Platform trust strip: static.
12. App / ecosystem CTA: static.

## `/news/` IA

The listing page must function as the main Intelligence Feed / virtual section hub. Topic-filtered URLs should feel like section pages even without new models.

Required order:

1. Compact section command header.
2. Section identity metrics.
3. Horizontal topic filters.
4. Dynamic featured lead story.
5. Live updates module.
6. Signal score module.
7. Dynamic article grid with varied hierarchy.
8. Trending topics.
9. Tracker rows.
10. Research/documents.
11. Analysis/video brief.
12. Expert perspective.
13. North Signal Brief.
14. Pagination.

Feed rhythm:

- First article: featured story.
- Second article: wide story.
- Next articles: mixed standard and compact cards.
- If article count is low, avoid empty grid slots and let static intelligence modules fill the product surface.

## Article IA

The article page remains an intelligence briefing.

Order:

1. Breadcrumbs/context.
2. Topic and signal tags.
3. Headline.
4. Dek.
5. Byline/date/read time.
6. Action controls.
7. Hero media/fallback visual.
8. Context rail.
9. Body.
10. Pull quote / inline intelligence module.
11. Right rail.
12. Related stories.

Rules:

- Body readability stays central.
- Context modules support the article; they do not replace content.
- If content is short, do not create fake article copy.

## Mobile IA

Mobile should feel like a compact intelligence app:

1. Compact brand bar.
2. Live ticker.
3. Status metrics as horizontal cards.
4. Page hero/story card.
5. Chips/action row.
6. Primary feed/content.
7. Context widgets.
8. CTA/footer.
9. Bottom nav with safe-area padding.

Mobile listing order:

1. Section title and dek.
2. Topic chips.
3. Featured story compact.
4. Dynamic story feed.
5. Latest Signals / rail modules.
6. Research/analysis widgets.

## Dynamic vs Static

Dynamic:

- Homepage lead article.
- Homepage latest signals.
- Homepage top stories.
- Listing featured story.
- Listing article grid.
- Article title, dek, body, date, author, topic, image.
- Related pages.

Static fallback:

- Ticker/status values.
- AI model tracker.
- Watchlist.
- Signal map.
- Trending signals/topics.
- Market snapshots.
- Research/document rows.
- North Signal Brief.
- App CTA.
