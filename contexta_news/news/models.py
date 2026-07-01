from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, HelpPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable
from wagtail.search import index

from wagtail.fields import StreamField
from contexta_news.utils.models import BasePage, ArticleTopic
from contexta_news.utils.blocks import CaptionedImageBlock, StoryBlock


class ImpactLevel(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class ConfidenceLevel(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    VERIFIED = "verified", "Verified"


class TimeSensitivity(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"


class ArticlePage(BasePage):
    template = "pages/article_page.html"
    parent_page_types = ["news.NewsListingPage"]

    author = models.ForeignKey(
        "utils.AuthorSnippet",
        blank=False,
        null=False,
        on_delete=models.deletion.PROTECT,
        related_name="+",
    )
    topic = models.ForeignKey(
        "utils.ArticleTopic",
        blank=False,
        null=False,
        on_delete=models.deletion.PROTECT,
        related_name="article_pages",
    )
    publication_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Use this field to override the date that the "
        "news item appears to have been published.",
    )
    introduction = models.TextField(blank=True)
    image = StreamField(
        [("image", CaptionedImageBlock())],
        blank=True,
        max_num=1,
    )
    body = StreamField(StoryBlock())
    featured_section_title = models.TextField(blank=True)
    impact_level = models.CharField(
        max_length=16,
        choices=ImpactLevel.choices,
        blank=True,
        help_text="Editorial impact label shown in article badges and intelligence cards.",
    )
    signal_score = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Numeric signal score, for example 91.8.",
    )
    confidence_level = models.CharField(
        max_length=16,
        choices=ConfidenceLevel.choices,
        blank=True,
    )
    source_confidence = models.CharField(
        max_length=16,
        choices=ConfidenceLevel.choices,
        blank=True,
    )
    time_sensitivity = models.CharField(
        max_length=16,
        choices=TimeSensitivity.choices,
        blank=True,
    )
    article_context_label = models.CharField(
        max_length=120,
        blank=True,
        help_text="Context label such as AI Infrastructure, Policy & Regulation, or Market Intelligence.",
    )
    intelligence_note = models.TextField(blank=True)
    pull_quote = models.TextField(blank=True)
    pull_quote_attribution = models.CharField(max_length=120, blank=True)
    pull_quote_source_label = models.CharField(max_length=160, blank=True)
    impact_model_title = models.CharField(max_length=120, blank=True)
    impact_model_metric_value = models.CharField(max_length=40, blank=True)
    impact_model_metric_label = models.CharField(max_length=80, blank=True)
    impact_model_secondary_metric = models.CharField(max_length=120, blank=True)
    impact_model_notes = models.TextField(blank=True)
    impact_model_source = models.CharField(max_length=160, blank=True)

    search_fields = BasePage.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("article_context_label"),
        index.SearchField("intelligence_note"),
        index.FilterField("topic"),
    ]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("author"),
                FieldPanel("publication_date"),
                FieldPanel("topic"),
                FieldPanel("introduction"),
                FieldPanel("body"),
            ],
            heading="Core Article",
        ),
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("listing_image"),
                FieldPanel("listing_title"),
                FieldPanel("listing_summary"),
            ],
            heading="Visuals / Media",
        ),
        MultiFieldPanel(
            [
                FieldPanel("article_context_label"),
                FieldPanel("intelligence_note"),
                FieldPanel("pull_quote"),
                FieldPanel("pull_quote_attribution"),
                FieldPanel("pull_quote_source_label"),
            ],
            heading="Intelligence Briefing",
        ),
        MultiFieldPanel(
            [
                FieldPanel("impact_level"),
                FieldPanel("signal_score"),
                FieldPanel("confidence_level"),
                FieldPanel("source_confidence"),
                FieldPanel("time_sensitivity"),
            ],
            heading="Signals & Impact",
        ),
        MultiFieldPanel(
            [
                FieldPanel("impact_model_title"),
                FieldPanel("impact_model_metric_value"),
                FieldPanel("impact_model_metric_label"),
                FieldPanel("impact_model_secondary_metric"),
                FieldPanel("impact_model_notes"),
                FieldPanel("impact_model_source"),
            ],
            heading="Inline Impact Model / Data Card",
        ),
        MultiFieldPanel(
            [
                InlinePanel("key_takeaways", label="Key takeaways"),
                InlinePanel("signal_tags", label="Signal tags"),
                InlinePanel("intelligence_related_signals", label="Related signals"),
            ],
            heading="Related Intelligence",
        ),
        MultiFieldPanel(
            [
                FieldPanel("featured_section_title", heading="Title"),
                InlinePanel(
                    "page_related_pages",
                    label="Pages",
                    max_num=3,
                ),
            ],
            heading="Featured section",
        ),
    ]

    @property
    def display_date(self):
        if self.publication_date:
            return self.publication_date.strftime("%d %b %Y")
        elif self.first_published_at:
            return self.first_published_at.strftime("%d %b %Y")

    @property
    def impact_display(self):
        return self.get_impact_level_display() if self.impact_level else "High"

    @property
    def confidence_display(self):
        return self.get_confidence_level_display() if self.confidence_level else "High"

    @property
    def source_confidence_display(self):
        return (
            self.get_source_confidence_display()
            if self.source_confidence
            else "High"
        )

    @property
    def time_sensitivity_display(self):
        return (
            self.get_time_sensitivity_display()
            if self.time_sensitivity
            else "30-90 days"
        )


class ArticleKeyTakeaway(Orderable):
    page = ParentalKey(
        ArticlePage,
        on_delete=models.CASCADE,
        related_name="key_takeaways",
    )
    label = models.CharField(max_length=80, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel("label"),
        FieldPanel("text"),
    ]

    def __str__(self):
        return self.text


class ArticleSignalTag(Orderable):
    page = ParentalKey(
        ArticlePage,
        on_delete=models.CASCADE,
        related_name="signal_tags",
    )
    label = models.CharField(max_length=80)

    panels = [FieldPanel("label")]

    def __str__(self):
        return self.label


class ArticleRelatedSignal(Orderable):
    page = ParentalKey(
        ArticlePage,
        on_delete=models.CASCADE,
        related_name="intelligence_related_signals",
    )
    signal = models.ForeignKey(
        "intelligence.LiveSignal",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    fallback_title = models.CharField(
        max_length=160,
        blank=True,
        help_text="Used when no Live Signal is selected.",
    )
    fallback_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional internal path or full URL for the fallback title.",
    )

    panels = [
        FieldPanel("signal"),
        FieldPanel("fallback_title"),
        FieldPanel("fallback_url"),
    ]

    def __str__(self):
        if self.signal:
            return self.signal.title
        return self.fallback_title or "Related signal"

    @property
    def title(self):
        if self.signal:
            return self.signal.title
        return self.fallback_title

    @property
    def link_url(self):
        if self.signal:
            return self.signal.link_url
        return self.fallback_url or "/news/"


class NewsListingPage(BasePage):
    template = "pages/news_listing_page.html"
    subpage_types = ["news.ArticlePage"]
    max_count = 1  # Allow only one news listing page to keep article pages in one place

    introduction = RichTextField(
        blank=True, features=["bold", "italic", "link"]
    )

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    content_panels = (
        BasePage.content_panels
        + [
            FieldPanel("introduction"),
            # FieldPanel("featured_card"),
            HelpPanel("This page will automatically display child Article pages."),
        ]
    )

    def paginate_queryset(self, queryset, request):
        """Paginate the queryset."""
        page_number = request.GET.get("page", 1)
        paginator = Paginator(queryset, settings.DEFAULT_PER_PAGE)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return (paginator, page, page.object_list, page.has_other_pages())


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        queryset = (
            ArticlePage.objects.live()
            .public()
            .annotate(
                date=Coalesce("publication_date", "first_published_at"),
            )
            .select_related("listing_image", "author", "topic")
            .order_by("-date")
        )

        article_topics = ArticleTopic.objects.filter(
            article_pages__isnull=False
        ).values("title", "slug").distinct().order_by("title")
        matching_topic = False

        topic_query_param = request.GET.get("topic")
        if topic_query_param and topic_query_param in article_topics.values_list(
            "slug", flat=True
        ):
            matching_topic = topic_query_param
            queryset = queryset.filter(topic__slug=topic_query_param)


        # Paginate article pages
        paginator, page, _object_list, is_paginated = self.paginate_queryset(
            queryset, request
        )
        context["paginator"] = paginator
        context["paginator_page"] = page
        context["is_paginated"] = is_paginated

        # Topics
        context["topics"] = article_topics
        context["matching_topic"] = matching_topic

        return context
