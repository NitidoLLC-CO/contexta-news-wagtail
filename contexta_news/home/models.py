from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index

from wagtail.fields import StreamField
from contexta_news.utils.blocks import StoryBlock, InternalLinkBlock
from contexta_news.utils.models import BasePage


class HomePage(BasePage):
    template = "pages/home_page.html"
    introduction = models.TextField(blank=True)
    hero_cta = StreamField(
        [("link", InternalLinkBlock())],
        blank=True,
        min_num=0,
        max_num=1,
    )
    body = StreamField(StoryBlock())
    featured_section_title = models.TextField(blank=True)

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("hero_cta"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("featured_section_title", heading="Title"),
                InlinePanel(
                    "page_related_pages",
                    label="Pages",
                    max_num=12,
                ),
            ],
            heading="Featured section",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        from contexta_news.news.models import ArticlePage

        articles = list(
            ArticlePage.objects.live()
            .public()
            .select_related("listing_image", "author", "topic")
            .order_by("-first_published_at")[:12]
        )

        context["lead_article"] = articles[0] if articles else None
        context["latest_signals"] = articles[1:5]
        context["top_stories"] = articles[1:7] or articles[:6]
        context["policy_stories"] = [
            article for article in articles if "policy" in article.topic.title.lower()
        ][:3]
        context["company_stories"] = [
            article
            for article in articles
            if any(
                term in article.topic.title.lower()
                for term in ("company", "companies", "model", "technology", "ai")
            )
        ][:3]

        return context
