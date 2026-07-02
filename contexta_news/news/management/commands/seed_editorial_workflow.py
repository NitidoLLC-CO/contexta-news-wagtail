from django.core.management.base import BaseCommand
from django.utils import timezone

from contexta_news.news.models import (
    ArticlePage,
    ArticleSourceReference,
    ConfidenceLevel,
    EditorialStatus,
    SourceReferenceType,
    SourceStatus,
    UrgencyLevel,
    VerificationStatus,
)


SOURCE_ROWS = [
    {
        "title": "Railway deployment verification record",
        "url": "https://contexta-news-wagtail-production.up.railway.app/news/deployment-test-article/",
        "source_type": SourceReferenceType.OFFICIAL,
        "confidence": ConfidenceLevel.VERIFIED,
        "is_primary": True,
        "note": "Primary production URL used to verify the live article workflow.",
    },
    {
        "title": "CONTEXTRA internal deployment analysis",
        "url": "https://contexta-news-wagtail-production.up.railway.app/admin/",
        "source_type": SourceReferenceType.OTHER,
        "confidence": ConfidenceLevel.HIGH,
        "is_primary": False,
        "note": "Internal editorial review reference for admin workflow validation.",
    },
    {
        "title": "Wagtail publishing workflow check",
        "url": "https://contexta-news-wagtail-production.up.railway.app/news/",
        "source_type": SourceReferenceType.OFFICIAL,
        "confidence": ConfidenceLevel.HIGH,
        "is_primary": False,
        "note": "Confirms the article remains visible in the public news feed.",
    },
]


class Command(BaseCommand):
    help = "Seed representative CONTEXTRA editorial production workflow data."

    def handle(self, *args, **options):
        article = (
            ArticlePage.objects.filter(slug="deployment-test-article").first()
            or ArticlePage.objects.filter(title__icontains="Deployment Test Article").first()
        )
        if article is None:
            self.stderr.write("Deployment test article not found. No workflow data seeded.")
            return

        article.editorial_status = EditorialStatus.VERIFIED
        article.verification_status = VerificationStatus.VERIFIED
        article.source_status = SourceStatus.INTERNAL_ANALYSIS
        article.urgency_level = UrgencyLevel.DEVELOPING
        article.editorial_priority = 92
        article.promote_on_homepage = True
        article.promote_in_section = True
        article.show_in_live_signals = True
        article.show_as_breaking = False
        article.include_in_newsletter = True
        article.ai_generated_draft = True
        article.ai_researched = True
        article.ai_fact_checked = True
        article.human_review_required = True
        article.human_reviewed = True
        article.production_agent_name = "Codex"
        article.editorial_reviewer = "CONTEXTRA Editorial Desk"
        article.last_reviewed_at = timezone.now()
        article.headline_checked = True
        article.sources_checked = True
        article.image_checked = True
        article.legal_risk_checked = True
        article.seo_checked = True
        article.mobile_preview_checked = True
        article.final_editorial_approval = True
        article.internal_editorial_note = (
            "Seeded as the canonical Phase 2H deployment-test workflow article."
        )
        article.verification_note = (
            "Production URL, article rendering, admin editability, and source references verified."
        )
        article.source_note = (
            "Representative source rows are seeded for workflow validation and can be replaced by editors."
        )
        article.save()

        for index, source in enumerate(SOURCE_ROWS):
            ArticleSourceReference.objects.update_or_create(
                page=article,
                title=source["title"],
                defaults={
                    "url": source["url"],
                    "source_type": source["source_type"],
                    "confidence": source["confidence"],
                    "is_primary": source["is_primary"],
                    "note": source["note"],
                    "sort_order": index,
                },
            )

        article.save_revision().publish()
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded editorial workflow for '{article.title}' with {len(SOURCE_ROWS)} source references."
            )
        )
