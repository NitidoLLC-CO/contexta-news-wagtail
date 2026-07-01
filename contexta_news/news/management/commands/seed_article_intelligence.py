from django.core.management.base import BaseCommand

from contexta_news.intelligence.models import LiveSignal
from contexta_news.news.models import (
    ArticleKeyTakeaway,
    ArticlePage,
    ArticleRelatedSignal,
    ArticleSignalTag,
)


class Command(BaseCommand):
    help = "Seed article-specific intelligence data for the deployment test article."

    def handle(self, *args, **options):
        article = ArticlePage.objects.filter(slug="deployment-test-article").first()
        if article is None:
            self.stderr.write("No article found with slug deployment-test-article.")
            return

        article.impact_level = "high"
        article.signal_score = "91.8"
        article.confidence_level = "high"
        article.source_confidence = "high"
        article.time_sensitivity = "high"
        article.article_context_label = "AI Infrastructure"
        article.intelligence_note = (
            "This briefing is structured for rapid context, decision support, "
            "and deeper editorial reading around deployment readiness."
        )
        article.pull_quote = (
            "The signal is not one event. It is the convergence of "
            "infrastructure, policy, capital, and deployment speed."
        )
        article.pull_quote_attribution = "CONTEXTRA Intelligence Desk"
        article.pull_quote_source_label = "Editorial analysis"
        article.impact_model_title = "Impact model"
        article.impact_model_metric_value = "91.8"
        article.impact_model_metric_label = "Signal strength"
        article.impact_model_secondary_metric = "30-90 days"
        article.impact_model_notes = (
            "High relevance across infrastructure, policy, and market exposure."
        )
        article.impact_model_source = "CONTEXTRA editorial model"
        article.save()

        takeaway_rows = [
            (
                "Infrastructure",
                "Infrastructure pressure is becoming a strategic variable.",
            ),
            (
                "Policy",
                "Policy, compute, and capital are converging quickly.",
            ),
            (
                "Markets",
                "Market response depends on supply reliability.",
            ),
        ]
        created_takeaways = 0
        for index, (label, text) in enumerate(takeaway_rows):
            _, created = ArticleKeyTakeaway.objects.get_or_create(
                page=article,
                text=text,
                defaults={"label": label, "sort_order": index},
            )
            created_takeaways += int(created)

        tag_labels = [
            "HIGH IMPACT",
            "POLICY SHIFT",
            "AI INFRASTRUCTURE",
            "MARKET SIGNAL",
            "SOURCE CONFIDENCE: HIGH",
        ]
        created_tags = 0
        for index, label in enumerate(tag_labels):
            _, created = ArticleSignalTag.objects.get_or_create(
                page=article,
                label=label,
                defaults={"sort_order": index},
            )
            created_tags += int(created)

        created_related = 0
        for index, signal in enumerate(LiveSignal.objects.active()[:3]):
            _, created = ArticleRelatedSignal.objects.get_or_create(
                page=article,
                signal=signal,
                defaults={"sort_order": index},
            )
            created_related += int(created)

        article.save_revision().publish()

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded article intelligence for deployment-test-article "
                f"(takeaways created={created_takeaways}, "
                f"tags created={created_tags}, "
                f"related signals created={created_related})."
            )
        )
