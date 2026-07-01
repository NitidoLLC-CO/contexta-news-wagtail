# 03 Visual System Notes

## Direction

The visual system must become richer than dark cards with cyan borders. The approved references use a dense command-center language: real brand marks, layered media, glass panels, data grids, micro metrics, watchlist rows, map surfaces, compact labels, and mobile product navigation.

## System Layers

### Tokens

Keep the current palette and expand semantic usage:

- Dark base: `--cx-bg`, `--cx-bg-deep`, `--cx-bg-soft`
- Panels: `--cx-panel`, `--cx-panel-glass`, `--cx-panel-strong`
- Borders/glow: `--cx-border`, `--cx-border-strong`, `--cx-glow`
- Brand: `--cx-cyan`, `--cx-blue`
- State: `--cx-green`, `--cx-red`, `--cx-amber`

### Brand Assets

Use optimized real brand assets derived from the branding folder:

- Header lockup/icon.
- Footer lockup/icon.
- North Signal app CTA.
- Card/media fallback watermark.
- Mobile bottom nav center mark.

### Surfaces

Introduce stronger reusable treatments:

- `.cx-surface`
- `.cx-command-panel`
- `.cx-glass-panel`
- `.cx-rail-panel`
- `.cx-metric-card`
- `.cx-signal-panel`

These should layer:

- translucent panel fill
- thin glowing border
- inner highlight
- data-grid pseudo-element
- subtle radial glow

### North Signal Visual

Current `contextra-signal-visual` is useful but overused. Add richer variations:

- hero
- compact card fallback
- watermark
- app CTA visual
- map/radar visual

Visuals should include micro labels, dots, orbit lines, and asset watermark so panels do not feel empty.

### Cards

Cards need hierarchy:

- standard story
- wide story
- compact signal row
- featured lead
- rail signal
- metric card

Every card needs either real image or dense fallback visual. Plain `CONTEXTRA` text placeholders are not acceptable.

### Mobile

Mobile gets explicit product rules:

- header remains compact with visible mark
- status metrics scroll horizontally
- chips scroll horizontally
- story cards become dense feed rows where needed
- decorative full holograms are hidden or converted to watermarks
- bottom nav is fixed, safe-area-aware, and content receives bottom padding

## Template Implications

Update:

- Header/footer to use real assets and bottom nav.
- Homepage for dense module rhythm.
- Listing page for section command-center layout.
- Article page for consistency only.
- Shared card components for fallback visuals and variants.

Do not touch backend models or deployment settings.
