# CONTEXTRA Article Intelligence Workflow

Phase 2E makes each Wagtail article editable as a CONTEXTRA intelligence briefing while preserving existing article URLs, publishing, media, and the accepted public visual design.

## Fields Added To Articles

The existing `ArticlePage` model now includes article-specific intelligence fields:

- `impact_level`: low, medium, high, critical.
- `signal_score`: numeric score such as `91.8`.
- `confidence_level`: low, medium, high, verified.
- `source_confidence`: low, medium, high, verified.
- `time_sensitivity`: low, medium, high, urgent.
- `article_context_label`: short context such as AI Infrastructure or Policy & Regulation.
- `intelligence_note`: short note shown near the top of the article body.
- `pull_quote`, `pull_quote_attribution`, `pull_quote_source_label`.
- Inline impact model fields:
  - `impact_model_title`
  - `impact_model_metric_value`
  - `impact_model_metric_label`
  - `impact_model_secondary_metric`
  - `impact_model_notes`
  - `impact_model_source`

## Ordered Editorial Rows

Three ordered child models were added for article-level briefing data:

- `ArticleKeyTakeaway`: label plus takeaway text.
- `ArticleSignalTag`: display tag such as HIGH IMPACT or POLICY SHIFT.
- `ArticleRelatedSignal`: optional link to a `LiveSignal` snippet, with manual fallback title/URL.

## Wagtail Admin Panels

The article editor is grouped into:

- Core Article
- Visuals / Media
- Intelligence Briefing
- Signals & Impact
- Inline Impact Model / Data Card
- Related Intelligence
- Featured section

Editors should fill the intelligence fields when an article needs to read as a briefing. Empty fields are safe.

## Frontend Mapping

The article template now uses article-specific fields for:

- Hero signal tags.
- Article context label.
- Hero signal score micro-panel.
- Key Takeaways.
- Related Topics.
- Trustbar confidence/source confidence.
- Intelligence Note.
- Pull Quote.
- Inline Signal Intelligence card.
- Article Intelligence score card.
- Briefing Status side card.
- Related Signals.
- Tags.

Market Snapshot remains snippet-backed from Phase 2D.

## Fallback Behavior

If any article intelligence fields are empty, the article page keeps the accepted static fallback copy. Existing old articles continue to render without requiring data migration.

## Seed Command

Run:

```powershell
python manage.py seed_article_intelligence
```

The command populates the existing `deployment-test-article` with representative article intelligence data. It is idempotent and will not duplicate key takeaways, signal tags, or related signals.

## Future Improvements

- Add per-article action configuration if Listen/Save/Cite become real product features.
- Add reusable intelligence templates for common article types.
- Add validation or editorial guidance for signal score ranges.
- Add richer relation rules between articles, Live Signals, topics, research briefs, and market watchlist items.
