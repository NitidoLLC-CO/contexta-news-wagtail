# 04 Mobile QA

## Mobile Target

The approved mobile reference behaves like a compact intelligence app, not a stacked desktop page. The rebuild implements:

- compact brand shell with visible North Signal mark
- live ticker below header
- horizontally scrollable status metrics
- safe-area-aware fixed bottom navigation
- horizontally scrollable filter chips
- dense story/feed cards
- hidden or compacted decorative visuals where they would delay useful content
- rails and intelligence modules stacked below primary content

## Homepage Mobile Rules

- Lead story remains the first meaningful content after shell/ticker.
- Lead metrics scroll horizontally instead of becoming a tall block.
- Large decorative micro-panels are suppressed on small screens.
- Top Stories and intelligence modules stack into a single column.
- Bottom navigation adds body padding so content is not covered.

## Listing Mobile Rules

- `/news/` starts with section title, dek, and metrics, not a giant empty visual.
- Section visual is hidden on mobile; brand identity stays in the top shell and bottom nav.
- Topic filters scroll horizontally.
- Featured story appears before static rail modules.
- Dynamic feed cards stack without horizontal overflow.
- Live updates, trackers, video brief, North Signal Brief, research, analysis, and events stack after the lead/feed.

## Article Mobile Rules

- Article headline appears early.
- Hero visual remains capped.
- Action chips scroll horizontally.
- Context and intelligence rails stack below the main article content.
- Body typography stays readable.

## Known Limits

- Bottom nav links are static public navigation targets for now.
- Listen/save/cite remain visual affordances until product behavior is implemented.
- Market/watchlist/research modules are static fallback data.
