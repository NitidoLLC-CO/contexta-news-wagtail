# CONTEXTRA Editorial Production Workflow

Phase 2H turns articles into production-managed intelligence briefings without redesigning the public frontend or changing Railway deployment.

## Fields Added

`ArticlePage` now includes editorial production metadata:

- `editorial_status`: idea, assigned, AI drafted, in review, verified, ready to publish, published, archived.
- `verification_status`: unverified, source checked, cross checked, legally sensitive, verified, disputed.
- `source_status`: single source, multi source, official source, primary document, wire verified, internal analysis.
- `urgency_level`: normal, developing, urgent, breaking.
- `editorial_priority`: 0-100 numeric priority used for promotion ordering.

Promotion flags:

- `promote_on_homepage`
- `promote_in_section`
- `show_in_live_signals`
- `show_as_breaking`
- `include_in_newsletter`

AI production metadata:

- `ai_generated_draft`
- `ai_researched`
- `ai_fact_checked`
- `human_review_required`
- `human_reviewed`
- `production_agent_name`
- `editorial_reviewer`
- `last_reviewed_at`

Internal notes:

- `internal_editorial_note`
- `verification_note`
- `source_note`

Production checklist:

- `headline_checked`
- `sources_checked`
- `image_checked`
- `legal_risk_checked`
- `seo_checked`
- `mobile_preview_checked`
- `final_editorial_approval`

## Source Workflow

Articles now support ordered source/reference rows through `ArticleSourceReference`.

Each row includes:

- title
- URL
- source type: official, company, government, wire, research, social, other
- confidence: low, medium, high, verified
- primary-source flag
- internal source note

These rows are for editorial production and verification. They are not shown publicly in Phase 2H.

## Admin Workflow

The article editor now has clear production groups:

- Core Article
- Visuals / Media
- Intelligence Briefing
- Signals & Impact
- Inline Impact Model / Data Card
- Editorial Workflow
- Verification & Sources
- AI Production Metadata
- Internal Notes
- Related Intelligence
- Featured section

Internal notes and source references are admin-only unless explicitly mapped in a later public template phase.

## Promotion Logic

Homepage article selection now prefers:

1. live/public articles with `promote_on_homepage=True`, ordered by `editorial_priority` and date
2. latest live/public articles as fallback

Section pages now prefer:

1. matching live/public articles with `promote_in_section=True`, ordered by `editorial_priority` and date
2. other matching live/public articles ordered by priority/date
3. latest live/public articles as fallback

Old articles remain safe because all workflow fields have defaults.

## Public Frontend Impact

No visual redesign was made.

Article pages may now show safe public badges derived from workflow metadata:

- Breaking or Developing
- Verified or Cross checked
- Official source or Primary document

Internal notes, source notes, reviewer names, and source reference rows are not exposed publicly.

## Seed Command

Run:

```powershell
python manage.py seed_editorial_workflow
```

The command updates the deployment test article with representative workflow data and three source references. It is idempotent and updates existing source rows by title instead of duplicating them.

## Future Improvements

- Add Wagtail workflow tasks for editor/reviewer handoff.
- Add reporting views for unverified, legally sensitive, or high-priority articles.
- Expose verified-source badges more richly once editorial policy is finalized.
- Connect `show_in_live_signals` to a public breaking/live article rail.
- Add source-reference public display for articles that are meant to be transparent briefings.
