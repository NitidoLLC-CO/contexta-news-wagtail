# 01 Current Gap Audit

## Verdict

The current CONTEXTRA public theme is directionally correct but not reference-grade. It still reads as a dark Wagtail/news template with cyan panels instead of the dense, cinematic intelligence platform shown in the approved references.

The core problem is credibility: too many modules reuse the same glass-card pattern, too many visuals are empty CSS placeholders, the real brand assets are not present in the public shell, and the mobile experience is mostly desktop content stacked downward.

## References Reviewed

- `contexctra branding/CONTEXTA_FUTURE_THEME_CODEX_PROMPT.md`
- `contexctra branding/740c0733-b5d3-46c5-ad23-8f532a17c6cf.png`
- `contexctra branding/17f73ba7-5054-4717-aedd-ec46dc867814.png`
- `contexctra branding/logo.png`
- `contexctra branding/profile logo.png`

## What Works

- Global shell already has brand area, nav, search, ticker, and status strip.
- Homepage includes the required module names and basic structure.
- Article page is a usable foundation for an intelligence briefing.
- Listing page has a featured story and feed structure.
- CSS tokens already establish the dark navy / cyan palette.

## Critical Gaps

### Brand Asset Gap

The references use a sharp, premium North Signal / CONTEXTRA mark. The current site uses a CSS-drawn approximation in the header/footer and repeated hologram panels. This weakens the first impression and makes the product feel coded rather than branded.

Required rebuild:

- Use optimized real brand assets for header, footer, app CTA, and visual watermarks.
- Keep CSS fallback mark only as a secondary emergency fallback.

### Homepage Gap

The homepage has sections, but visual density is still shallow. The reference has a command-center composition where media, metrics, live signals, watchlists, maps, research, and app CTA all feel distinct. Current modules feel like repeated cards with cyan borders.

Required rebuild:

- Tighten first fold into a complete system: lead story, cinematic visual, live rail, status/metrics, and next section visible.
- Give static widgets stronger internal structure, micro-labels, sparklines, rows, and visual density.
- Replace plain placeholder surfaces with North Signal / data-grid fallback visuals.

### Listing Page Gap

`/news/` is the weakest page. It is still a dressed-up archive/feed, not a section command center like the `Policy & Power` reference.

Required rebuild:

- Section command header, not a giant "News" card.
- Dynamic featured story.
- Filter chips.
- Live updates rail.
- Signal score.
- Trending topics.
- Policy/AI trackers.
- Research/documents.
- Video/deep-dive block.
- Expert perspective.
- Events/briefing CTA.
- Dense mobile-first story list.

### Article Page Gap

The article page has the right layout direction, but too many modules are fake and repetitive.

Required refinements:

- Improve hero visual density.
- Make actions less misleading by keeping them visual affordances but clearly non-destructive.
- Add useful market/related signal modules without overworking article body.
- Keep body readability central.

### Mobile Gap

Mobile does not yet match the reference app-like experience.

Problems:

- Brand mark disappears on small screens.
- No bottom mobile nav.
- Listing page starts with an oversized card and not enough immediate feed utility.
- Status/ticker rows are compact but not product-like.
- Article actions are text chips, not mobile controls.

Required rebuild:

- Preserve brand mark on mobile.
- Add safe-area-aware mobile bottom nav.
- Use horizontal metric/chip scrollers intentionally.
- Make listing first viewport useful: title, filters, featured compact story.
- Stack cards as dense mobile feed items.

## Starter Template Leakage

Public utility pages and streamfield blocks still contain old Wagtail/Tailwind visual language, including `mackerel-*`, large starter typography, white surfaces, and generic rounded blocks. These are not the main sprint target but remain a risk for Phase 2D.

## Rebuild Priority

1. Brand shell with real assets.
2. Rich reusable visual system.
3. Homepage density and first fold.
4. `/news/` section hub rebuild.
5. Article consistency refinements.
6. Mobile product experience.
7. Public utility/streamfield cleanup in a later phase.
