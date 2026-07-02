# Phase 2I Reference Structure Audit

Source folder: `E:\Development\contextra_website\contexctra branding`

Reference assets reviewed:

- `740c0733-b5d3-46c5-ad23-8f532a17c6cf.png`
- `17f73ba7-5054-4717-aedd-ec46dc867814.png`
- `logo.png`
- `profile logo.png`
- `CONTEXTA_FUTURE_THEME_CODEX_PROMPT.md`

## Desktop Homepage Reference

File: `740c0733-b5d3-46c5-ad23-8f532a17c6cf.png`

Page type: desktop homepage / annotated guide.

Major layout zones:

- Outer framed application shell with tight content width and visible right annotation column.
- Header with brand lockup on the left, centered section navigation, search and icon actions on the right.
- Thin live signal ticker directly below the header.
- Compact status metrics strip below the ticker.
- Large first-fold hero system, not a standalone card.
- Hero composition has left editorial copy, central immersive cinematic visual, and right-side live signals rail.
- Top Stories row immediately follows the hero inside the first major dashboard slab.
- AI Models Tracker and Watchlist sit in the same upper dashboard band as Top Stories.
- Lower grid contains Signal Map, Trending Signals, Analysis & Insights, Research Briefs, and North Signal Brief.
- Footer feature strip sits above the app/ecosystem CTA.
- App CTA uses North Signal App, app-store badges, phone visual, and a wide CTA button.
- Footer is compact, dense, and integrated into the same visual system.

Module order:

1. Header / nav / search
2. Live Signal Ticker
3. Status Metrics Strip
4. Hero Lead Story plus immersive visual plus Live Signals rail
5. Top Stories plus AI Models Tracker plus Watchlist
6. Signal Map plus Trending Signals plus Analysis & Insights plus Research Briefs plus North Signal Brief
7. Footer Feature Strip
8. North Signal App / ecosystem CTA
9. Footer links and copyright

Grid structure:

- Desktop uses a dense 12-column style composition.
- Hero spans most of the width with right rail attached.
- Top Stories uses varied cards across the left/middle, with trackers stacked to the right.
- Lower modules are smaller equal-height panels, tightly spaced, and visually balanced.
- The page reads as a premium command-center newsroom rather than separate stacked sections.

First viewport composition:

- Header, ticker, status metrics, hero, right rail, and the top of Top Stories are visible in one screen.
- The hero visual is cinematic but contained; it does not force the story grid far below the fold.
- Micro metrics and story CTA live inside the hero composition.

Right rail modules:

- Live Signals rail is strong and visible in the hero.
- AI Models Tracker and Watchlist are close to the first fold.
- North Signal Brief is a lower-right conversion/intelligence module.

Footer/app CTA structure:

- Footer Feature Strip with four trust pillars.
- North Signal App panel with badges and device/app visual.
- Compact footer with brand mark and institutional links.

Mobile structure:

- Not represented in this file directly, but the homepage design implies compact top bar, ticker, hero card, live intelligence metrics, top stories, and bottom navigation as shown in the mobile reference.

Current implementation missing:

- Current homepage has the right colors and panels but is not dense enough.
- Hero is still too isolated and leaves lower modules feeling detached.
- Top Stories, AI tracker, and Watchlist are not integrated into one tight upper dashboard band.
- App CTA/footer strip need to be closer to the reference ordering and density.

## Mobile Experience Reference

File: `17f73ba7-5054-4717-aedd-ec46dc867814.png`

Page type: mobile annotated guide with home, section, and article examples.

Major layout zones:

- Compact top bar with centered CONTEXTRA branding and quick actions.
- Live Signal Ticker immediately below top bar.
- Mobile homepage hero story card with strong visual, headline, date chip, and CTA.
- Live intelligence metric cards directly under the hero.
- Top Stories list with chips and compact story cards.
- Section page with compact section title, smart filters, featured card, sorted feed, and bottom nav.
- Article page with compact article header, media block, action bar, body intro, quote/key takeaways, related story card, and bottom nav.
- Persistent bottom navigation with Home, Sections, center brand mark, Watchlist, Profile.

Module order:

Mobile home:

1. Compact brand top bar
2. Live Signal Ticker
3. Hero story card
4. Live intelligence metrics
5. Top Stories filter chips
6. Compact story cards
7. Bottom nav

Mobile section:

1. Compact brand top bar
2. Section title and subtitle
3. Horizontal category filters
4. Featured story card
5. Smart filters / sort
6. Stacked article cards
7. Bottom nav

Mobile article:

1. Compact top actions
2. Article category chip
3. Headline and metadata
4. Hero media block
5. Action chips
6. Body lead paragraph
7. Quote / key takeaways
8. Related story card
9. Bottom nav

Grid structure:

- Single-column mobile structure with horizontal chips where needed.
- Strong first card hierarchy.
- Cards are compact and content-rich, not large empty slabs.
- The bottom nav is persistent and does not cover key content.

First viewport composition:

- Homepage first viewport includes brand, ticker, most of hero, and beginning of live intelligence.
- Section first viewport includes title, chips, featured story.
- Article first viewport includes headline, metadata, visual, and action bar.

Right rail modules:

- Desktop right rails become stacked modules below the top feature on mobile.
- Live modules must appear early, not after large intro-only panels.

Footer/app CTA structure:

- Mobile footer is less prominent than bottom nav, but app ecosystem should still appear as a compact CTA lower down.

Current implementation missing:

- Mobile is clean but not structurally close enough.
- Current section mobile first viewport spends too much space on intro panels.
- Current mobile story cards need stronger hierarchy and more reference-like compactness.
- Bottom nav exists but labels/icons need to align with Home, Sections, Watchlist, Profile and center brand emphasis.

## Brand Identity Reference

File: `logo.png`

Page type: brand identity / North Signal concept board.

Major layout zones:

- North Signal symbol as an upward institutional mark.
- Horizontal CONTEXTRA lockup with descriptor `INTELLIGENCE NEWS`.
- Tagline: `INTELLIGENCE THAT LEADS. NEWS THAT MATTERS.`
- Powered by `NITIDO`.

Structural implications:

- Use the mark as a controlled brand element, not a repeated filler graphic everywhere.
- The symbol should provide authority and continuity, but page-specific visuals should vary by module/page type.
- Brand spacing and typography are precise, letter-spaced, institutional, and premium.

Current implementation missing:

- The mark appears too repeatedly as generic visual filler.
- Need more actual module imagery/abstract data visuals and less logo-only repetition.

## Profile Logo Reference

File: `profile logo.png`

Page type: dark luminous emblem asset.

Major layout zones:

- Single North Signal emblem on deep navy background.
- Blue glow and metallic edge treatment.

Structural implications:

- Best used for brand marks, bottom nav center mark, footer mark, and small watermark accents.
- Should not be the only hero visual across every page.

Current implementation missing:

- Need more page/module-specific data visuals around the mark instead of reusing it as the dominant visual in every section.

## Reference Summary

The approved design system is not just dark colors and cyan lines. It is a dense editorial command-center layout with:

- compressed first folds
- visible content in every major viewport
- strong right rails
- upper dashboard bands
- varied card sizes
- integrated intelligence widgets
- compact mobile hierarchy
- brand mark used with restraint

Phase 2I must rebuild public templates around this structure while preserving Wagtail content, snippets, section pages, article intelligence fields, and Phase 2H promotion logic.
