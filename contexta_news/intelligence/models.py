from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class ActiveOrderedQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ActiveOrderedModel(models.Model):
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(
        default=100,
        help_text="Lower numbers appear first.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveOrderedQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ["sort_order", "id"]


class ImpactLevel(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class SignalStatus(models.TextChoices):
    NEUTRAL = "neutral", "Neutral"
    ACTIVE = "active", "Active"
    BULLISH = "bullish", "Bullish"
    WARNING = "warning", "Warning"


@register_snippet
class LiveSignal(ActiveOrderedModel, index.Indexed):
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=80, blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    impact_level = models.CharField(
        max_length=16,
        choices=ImpactLevel.choices,
        default=ImpactLevel.HIGH,
    )
    summary = models.TextField(blank=True)
    url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional internal path or full URL.",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("category"),
        FieldPanel("published_at"),
        FieldPanel("impact_level"),
        FieldPanel("summary"),
        FieldPanel("url"),
        MultiFieldPanel(
            [FieldPanel("is_active"), FieldPanel("sort_order")],
            heading="Publishing controls",
        ),
    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("category"),
        index.SearchField("summary"),
    ]

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "live signal"
        verbose_name_plural = "live signals"

    def __str__(self):
        return self.title

    @property
    def impact_label(self):
        return f"{self.get_impact_level_display()} impact"

    @property
    def impact_badge_class(self):
        if self.impact_level in {ImpactLevel.LOW, ImpactLevel.MEDIUM}:
            return "cx-impact-badge--medium"
        return ""

    @property
    def link_url(self):
        return self.url or "/news/"


@register_snippet
class StatusMetric(ActiveOrderedModel, index.Indexed):
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=40)
    sublabel = models.CharField(max_length=120, blank=True)
    status = models.CharField(
        max_length=16,
        choices=SignalStatus.choices,
        default=SignalStatus.NEUTRAL,
    )
    sparkline = models.CharField(
        max_length=40,
        blank=True,
        help_text="Optional short value or visual hint, for example +2.1%.",
    )

    panels = [
        FieldPanel("label"),
        FieldPanel("value"),
        FieldPanel("sublabel"),
        FieldPanel("status"),
        FieldPanel("sparkline"),
        MultiFieldPanel(
            [FieldPanel("is_active"), FieldPanel("sort_order")],
            heading="Publishing controls",
        ),
    ]

    search_fields = [
        index.SearchField("label"),
        index.SearchField("value"),
        index.SearchField("sublabel"),
    ]

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "status metric"
        verbose_name_plural = "status metrics"

    def __str__(self):
        return f"{self.label}: {self.value}"

    @property
    def css_class(self):
        if self.status in {SignalStatus.ACTIVE, SignalStatus.BULLISH}:
            return "cx-positive"
        if self.status == SignalStatus.WARNING:
            return "cx-amber"
        return ""


class TrendLabel(models.TextChoices):
    RISING = "rising", "Rising"
    HIGH = "high", "High"
    MEDIUM = "medium", "Medium"
    LOW = "low", "Low"


@register_snippet
class TrendingTopic(ActiveOrderedModel, index.Indexed):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80, blank=True)
    signal_count = models.PositiveIntegerField(default=0)
    trend_label = models.CharField(
        max_length=16,
        choices=TrendLabel.choices,
        default=TrendLabel.RISING,
    )
    url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional internal path or full URL.",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("category"),
        FieldPanel("signal_count"),
        FieldPanel("trend_label"),
        FieldPanel("url"),
        MultiFieldPanel(
            [FieldPanel("is_active"), FieldPanel("sort_order")],
            heading="Publishing controls",
        ),
    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("category"),
    ]

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "trending topic"
        verbose_name_plural = "trending topics"

    def __str__(self):
        return self.title

    @property
    def link_url(self):
        return self.url or "/news/"


@register_snippet
class AIModelTrackerItem(ActiveOrderedModel, index.Indexed):
    model_name = models.CharField(max_length=120)
    provider = models.CharField(max_length=80, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=1)
    delta = models.CharField(max_length=24, blank=True)
    status = models.CharField(max_length=80, blank=True)
    icon_label = models.CharField(max_length=12, blank=True)

    panels = [
        FieldPanel("model_name"),
        FieldPanel("provider"),
        FieldPanel("score"),
        FieldPanel("delta"),
        FieldPanel("status"),
        FieldPanel("icon_label"),
        MultiFieldPanel(
            [FieldPanel("is_active"), FieldPanel("sort_order")],
            heading="Publishing controls",
        ),
    ]

    search_fields = [
        index.SearchField("model_name"),
        index.SearchField("provider"),
        index.SearchField("status"),
    ]

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "AI model tracker item"
        verbose_name_plural = "AI model tracker items"

    def __str__(self):
        return self.model_name


class DeltaDirection(models.TextChoices):
    UP = "up", "Up"
    DOWN = "down", "Down"
    NEUTRAL = "neutral", "Neutral"


@register_snippet
class MarketWatchlistItem(ActiveOrderedModel, index.Indexed):
    ticker = models.CharField(max_length=16)
    company_name = models.CharField(max_length=120)
    value = models.CharField(max_length=40, blank=True)
    delta = models.CharField(max_length=24, blank=True)
    delta_direction = models.CharField(
        max_length=16,
        choices=DeltaDirection.choices,
        default=DeltaDirection.NEUTRAL,
    )
    sector = models.CharField(max_length=80, blank=True)

    panels = [
        FieldPanel("ticker"),
        FieldPanel("company_name"),
        FieldPanel("value"),
        FieldPanel("delta"),
        FieldPanel("delta_direction"),
        FieldPanel("sector"),
        MultiFieldPanel(
            [FieldPanel("is_active"), FieldPanel("sort_order")],
            heading="Publishing controls",
        ),
    ]

    search_fields = [
        index.SearchField("ticker"),
        index.SearchField("company_name"),
        index.SearchField("sector"),
    ]

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "market/watchlist item"
        verbose_name_plural = "market/watchlist items"

    def __str__(self):
        return self.ticker

    @property
    def delta_class(self):
        if self.delta_direction == DeltaDirection.UP:
            return "cx-positive"
        if self.delta_direction == DeltaDirection.DOWN:
            return "cx-negative"
        return ""

    @property
    def sparkline_class(self):
        if self.delta_direction == DeltaDirection.DOWN:
            return "cx-sparkline--red"
        return ""


class DocumentType(models.TextChoices):
    REPORT = "report", "Report"
    BRIEFING = "briefing", "Briefing"
    RESEARCH = "research", "Research"
    PDF = "pdf", "PDF"
    LINK = "link", "Link"


@register_snippet
class ResearchBrief(ActiveOrderedModel, index.Indexed):
    title = models.CharField(max_length=160)
    summary = models.TextField(blank=True)
    category = models.CharField(max_length=80, blank=True)
    document_type = models.CharField(
        max_length=16,
        choices=DocumentType.choices,
        default=DocumentType.BRIEFING,
    )
    file = models.FileField(upload_to="research_briefs/", blank=True)
    external_url = models.URLField(blank=True)
    published_at = models.DateTimeField(default=timezone.now)

    panels = [
        FieldPanel("title"),
        FieldPanel("summary"),
        FieldPanel("category"),
        FieldPanel("document_type"),
        FieldPanel("file"),
        FieldPanel("external_url"),
        FieldPanel("published_at"),
        MultiFieldPanel(
            [FieldPanel("is_active"), FieldPanel("sort_order")],
            heading="Publishing controls",
        ),
    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("summary"),
        index.SearchField("category"),
    ]

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "research brief"
        verbose_name_plural = "research briefs"

    def __str__(self):
        return self.title

    @property
    def link_url(self):
        if self.external_url:
            return self.external_url
        if self.file:
            return self.file.url
        return "/news/"


@register_snippet
class NorthSignalBrief(index.Indexed, models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=160, blank=True)
    body = models.TextField(blank=True)
    cta_label = models.CharField(max_length=60, default="Preview brief")
    cta_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Internal path or full URL.",
    )
    email_placeholder = models.CharField(max_length=80, default="Enter your email")
    trust_text = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("body"),
        FieldPanel("cta_label"),
        FieldPanel("cta_url"),
        FieldPanel("email_placeholder"),
        FieldPanel("trust_text"),
        FieldPanel("is_active"),
    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("subtitle"),
        index.SearchField("body"),
    ]

    class Meta:
        ordering = ["-updated_at", "id"]
        verbose_name = "North Signal brief"
        verbose_name_plural = "North Signal briefs"

    def __str__(self):
        return self.title

    @property
    def link_url(self):
        return self.cta_url or "/news/"


@register_snippet
class AppEcosystemCTA(index.Indexed, models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=160, blank=True)
    body = models.TextField(blank=True)
    cta_label = models.CharField(max_length=60, default="Explore the app")
    cta_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Internal path or full URL.",
    )
    app_store_url = models.URLField(blank=True)
    google_play_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("body"),
        FieldPanel("cta_label"),
        FieldPanel("cta_url"),
        FieldPanel("app_store_url"),
        FieldPanel("google_play_url"),
        FieldPanel("is_active"),
    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("subtitle"),
        index.SearchField("body"),
    ]

    class Meta:
        ordering = ["-updated_at", "id"]
        verbose_name = "app/ecosystem CTA"
        verbose_name_plural = "app/ecosystem CTAs"

    def __str__(self):
        return self.title

    @property
    def link_url(self):
        return self.cta_url or "/news/"
