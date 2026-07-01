# Phase 2C-QA Lockdown Audit

Date: 2026-07-01

## Why Previous QA Was Invalid

The previous QA verdict was invalid because it marked the redesign as accepted without six clear screenshots. Mobile and article screenshots were missing, and the available desktop captures were visually soft. A visual redesign cannot be accepted without readable desktop and mobile evidence for the homepage, news listing, and article detail page.

## Screenshot Workflow Finding

The blurry screenshots were caused by the screenshot workflow, not by a global CSS blur. Firefox/Playwright captures are sharp and readable. The in-app browser capture channel became unreliable after navigation and screenshot timeouts, while Chromium-based renderers in this Windows session crashed with an access-violation exit code. Firefox is the reliable capture method for this QA pass.

## Live Page Sharpness

The actual rendered pages are visually sharp in Firefox. Text does not have global blur. The North Signal assets are readable at the intended sizes. Decorative media areas intentionally use glow/filter treatment, but body text, headings, nav labels, and cards remain crisp.

## Homepage

The homepage remains functional and aligned with the future intelligence-platform direction. The lead story, Latest Signals rail, and Top Stories section appear in the desktop first fold. The previous desktop hero text overlap was already corrected by constraining the lead story headline.

## Article Page

The article page remains functional and readable. The mobile article page shows the headline, metadata, actions, and hero image in a compact stack. Body content follows below without horizontal overflow.

## News Listing

The `/news/` page now uses a section-hub structure, not a plain archive. The desktop first fold shows section identity, North Signal visual, live updates, filter chips, and the beginning of the featured article. The right rail has dynamic Wagtail content plus static fallback signal links so it does not appear empty when the database has only one article.

## Issues Found

- Previous screenshot evidence was incomplete and too blurry for approval.
- Header icons contained mojibake characters.
- Mobile bottom navigation was inside the sticky/glass header, causing fixed positioning to anchor near the top in Firefox.
- `/news/` mobile had horizontal overflow because the live updates rail inherited a wider grid placement.
- `/news/` right rail was weak with only one article in the database.

## Fixes Applied

- Replaced mojibake icon text with ASCII-safe labels.
- Moved the mobile bottom navigation outside the sticky header so it fixes to the viewport bottom.
- Added mobile CSS to stack `/news/` command modules and prevent rail overflow.
- Added isolated fallback live-signal links to strengthen the news listing right rail.
- Rebuilt compiled CSS.

## QA Acceptance Rule

QA remains rejected until all six required screenshots exist in `tmp/qa-lockdown/` and are visually reviewed.

## Final Screenshot Evidence

Captured from the live Railway deployment using Firefox/Playwright at 1440x1000 desktop and 390x844 mobile viewports:

- `home-desktop.png`
- `home-mobile.png`
- `news-desktop.png`
- `news-mobile.png`
- `article-desktop.png`
- `article-mobile.png`

Final screenshot metrics:

- No horizontal overflow on homepage, news listing, or article detail at desktop or mobile widths.
- No broken images detected.
- Compiled production CSS loaded on all pages.
- North Signal compiled image assets loaded.

## Final QA Verdict

QA accepts the Phase 2C-QA Lockdown pass.

Remaining issues are scoped to later design/content phases: the static fallback intelligence widgets should eventually become Wagtail snippets or data-backed modules, and the deeper article body system can be expanded in a future phase. No Phase 2D work was started here.
