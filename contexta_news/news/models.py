from django.conf import settings
from django.db import models
from django.db.models import Q
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


class SectionVisualMode(models.TextChoices):
    AI_CORE = "ai-core", "AI core"
    CHIP_INFRASTRUCTURE = "chip-infrastructure", "Chip / infrastructure"
    POLICY_GOVERNMENT = "policy-government", "Policy / government"
    MARKET_CHART = "market-chart", "Market / chart"
    RESEARCH_NETWORK = "research-network", "Research / network"
    COMPANY_CLOUD = "company-cloud", "Company / cloud"


SECTION_VARIANTS = {
    SectionVisualMode.AI_CORE: {
        "visual_class": "ai-core",
        "visual_label": "AI CORE",
        "live_heading": "Model Signals",
        "live_subheading": "Agentic watch",
        "score_label": "Model relevance",
        "score_copy": "Tracking frontier systems, agents, benchmarks, and deployment pressure.",
        "trending_heading": "Benchmark Drift",
        "trending_window": "24h",
        "watchlist_heading": "Frontier Models",
        "watchlist_subheading": "Active systems",
        "research_heading": "Safety Signals",
        "research_subheading": "Evaluations",
        "analysis_heading": "Agent Infrastructure",
        "analysis_subheading": "AI systems",
        "analysis_title": "Monitor the model, agent, safety, and compute signals defining AI capability.",
        "feed_kicker": "AI Feed",
        "matched_heading": "Model and agent developments",
        "fallback_heading": "Latest AI-relevant intelligence",
        "feature_label": "Model context",
        "active_status": "Model scan active",
        "fallback_status": "AI fallback feed",
        "fallback_signals": [
            {"eyebrow": "Model layer", "title": "Frontier model release windows compress", "category": "Models"},
            {"eyebrow": "Agent layer", "title": "Enterprise agent deployments move into production", "category": "Agents"},
            {"eyebrow": "Safety", "title": "Evaluation coverage becomes a procurement signal", "category": "Benchmarks"},
        ],
        "fallback_topics": [
            {"title": "Long-context reasoning", "trend": "Rising"},
            {"title": "Agentic AI platforms", "trend": "High"},
            {"title": "Frontier model safety", "trend": "Active"},
        ],
        "fallback_watchlist": [
            {"ticker": "GPT", "value": "Models", "class": "cx-positive"},
            {"ticker": "AGT", "value": "Agents", "class": ""},
            {"ticker": "EVAL", "value": "Bench", "class": ""},
        ],
        "fallback_briefs": [
            {"title": "Frontier model capability brief", "age": "Live"},
            {"title": "Agent infrastructure watch", "age": "Live"},
            {"title": "AI safety evaluation notes", "age": "Live"},
        ],
        "module_rows": [
            {"label": "Frontier Models", "text": "Capability, release cadence, and context-window competition.", "status": "Live"},
            {"label": "Agent Infrastructure", "text": "Tool-use, orchestration, memory, and enterprise deployment.", "status": "Tracking"},
            {"label": "Safety Signals", "text": "Evaluations, incidents, and governance pressure around model behavior.", "status": "Watch"},
        ],
    },
    SectionVisualMode.CHIP_INFRASTRUCTURE: {
        "visual_class": "technology-grid",
        "visual_label": "COMPUTE GRID",
        "live_heading": "Infrastructure Updates",
        "live_subheading": "Chip signals",
        "score_label": "Infrastructure relevance",
        "score_copy": "Tracking chips, cloud capacity, data centers, networks, and compute constraints.",
        "trending_heading": "Cloud Capacity",
        "trending_window": "24h",
        "watchlist_heading": "Semiconductor Watch",
        "watchlist_subheading": "Compute layer",
        "research_heading": "Systems Briefs",
        "research_subheading": "Infrastructure",
        "analysis_heading": "Cloud Buildout",
        "analysis_subheading": "Technology",
        "analysis_title": "Track the hardware, cloud, data-center, and platform signals behind AI scale.",
        "feed_kicker": "Technology Feed",
        "matched_heading": "Compute and infrastructure developments",
        "fallback_heading": "Latest technology infrastructure intelligence",
        "feature_label": "Compute context",
        "active_status": "Grid scan active",
        "fallback_status": "Technology fallback feed",
        "fallback_signals": [
            {"eyebrow": "Compute", "title": "GPU demand remains the bottleneck for AI expansion", "category": "Chips"},
            {"eyebrow": "Cloud", "title": "Cloud providers reserve capacity for AI workloads", "category": "Cloud"},
            {"eyebrow": "Data centers", "title": "Power availability becomes a strategic infrastructure factor", "category": "Infrastructure"},
        ],
        "fallback_topics": [
            {"title": "GPU supply chains", "trend": "High"},
            {"title": "Cloud capacity auctions", "trend": "Rising"},
            {"title": "AI data-center power", "trend": "Active"},
        ],
        "fallback_watchlist": [
            {"ticker": "GPU", "value": "Tight", "class": "cx-positive"},
            {"ticker": "DC", "value": "Buildout", "class": ""},
            {"ticker": "PWR", "value": "Constraint", "class": "cx-negative"},
        ],
        "fallback_briefs": [
            {"title": "AI compute infrastructure brief", "age": "Live"},
            {"title": "Cloud capacity and data-center watch", "age": "Live"},
            {"title": "Semiconductor supply pressure notes", "age": "Live"},
        ],
        "module_rows": [
            {"label": "Semiconductor Watch", "text": "GPU supply, accelerators, packaging, and fabrication constraints.", "status": "Live"},
            {"label": "Cloud Buildout", "text": "Capacity reservations, AI regions, data-center power, and network scale.", "status": "Tracking"},
            {"label": "Systems Briefs", "text": "The hardware and software layers enabling frontier deployment.", "status": "Watch"},
        ],
    },
    SectionVisualMode.COMPANY_CLOUD: {
        "visual_class": "companies-network",
        "visual_label": "COMPETITIVE MAP",
        "live_heading": "Strategic Moves",
        "live_subheading": "Provider watch",
        "score_label": "Competitive relevance",
        "score_copy": "Tracking labs, providers, partnerships, funding, launches, and strategic deals.",
        "trending_heading": "Model Provider Watch",
        "trending_window": "24h",
        "watchlist_heading": "Funding Signals",
        "watchlist_subheading": "Company layer",
        "research_heading": "Product Launches",
        "research_subheading": "Companies",
        "analysis_heading": "Deals & Partnerships",
        "analysis_subheading": "Companies",
        "analysis_title": "Track the labs, providers, deal flow, partnerships, and competitive pressure moving AI.",
        "feed_kicker": "Companies Feed",
        "matched_heading": "Company and lab developments",
        "fallback_heading": "Latest company intelligence",
        "feature_label": "Competitive context",
        "active_status": "Company map active",
        "fallback_status": "Company fallback feed",
        "fallback_signals": [
            {"eyebrow": "Provider layer", "title": "Model providers compete on enterprise distribution", "category": "Providers"},
            {"eyebrow": "Funding", "title": "AI infrastructure financing concentrates around large labs", "category": "Capital"},
            {"eyebrow": "Partnerships", "title": "Cloud alliances define model access and deployment routes", "category": "Deals"},
        ],
        "fallback_topics": [
            {"title": "OpenAI and Microsoft alignment", "trend": "High"},
            {"title": "Anthropic enterprise expansion", "trend": "Rising"},
            {"title": "Nvidia ecosystem leverage", "trend": "Active"},
        ],
        "fallback_watchlist": [
            {"ticker": "OAI", "value": "Lab", "class": ""},
            {"ticker": "NVDA", "value": "Infra", "class": "cx-positive"},
            {"ticker": "MSFT", "value": "Cloud", "class": ""},
        ],
        "fallback_briefs": [
            {"title": "AI lab competitive map", "age": "Live"},
            {"title": "Strategic deal and partnership notes", "age": "Live"},
            {"title": "Model-provider market structure brief", "age": "Live"},
        ],
        "module_rows": [
            {"label": "Deals", "text": "Funding, acquisitions, cloud commitments, and model access agreements.", "status": "Live"},
            {"label": "Partnerships", "text": "Provider alliances, enterprise channels, and infrastructure relationships.", "status": "Tracking"},
            {"label": "Product Launches", "text": "Model releases, enterprise tools, platform bundles, and distribution shifts.", "status": "Watch"},
        ],
    },
    SectionVisualMode.POLICY_GOVERNMENT: {
        "visual_class": "policy-signal",
        "visual_label": "POLICY / GOVERNMENT",
        "live_heading": "Regulation Watch",
        "live_subheading": "Export controls",
        "score_label": "Policy relevance",
        "score_copy": "Tracking regulation, sovereignty, safety institutes, public adoption, and state power.",
        "trending_heading": "Sovereignty Signals",
        "trending_window": "24h",
        "watchlist_heading": "Government Actions",
        "watchlist_subheading": "Public sector",
        "research_heading": "Safety Institutes",
        "research_subheading": "Policy research",
        "analysis_heading": "Public Investment",
        "analysis_subheading": "Policy",
        "analysis_title": "Track the regulations, safety institutions, export controls, and public-sector AI signals.",
        "feed_kicker": "Policy Feed",
        "matched_heading": "Regulatory and government developments",
        "fallback_heading": "Latest policy intelligence",
        "feature_label": "Policy context",
        "active_status": "Policy scan active",
        "fallback_status": "Policy fallback feed",
        "fallback_signals": [
            {"eyebrow": "Regulation", "title": "AI rulemaking moves from principles to enforcement", "category": "Regulation"},
            {"eyebrow": "Export control", "title": "Compute restrictions reshape national AI strategies", "category": "Trade"},
            {"eyebrow": "Sovereignty", "title": "Governments fund domestic model and cloud capacity", "category": "Sovereignty"},
        ],
        "fallback_topics": [
            {"title": "AI sovereignty programs", "trend": "High"},
            {"title": "Export-control compliance", "trend": "Rising"},
            {"title": "Safety institute mandates", "trend": "Active"},
        ],
        "fallback_watchlist": [
            {"ticker": "ACT", "value": "Rules", "class": ""},
            {"ticker": "GOV", "value": "Spend", "class": "cx-positive"},
            {"ticker": "XCTL", "value": "Tight", "class": "cx-negative"},
        ],
        "fallback_briefs": [
            {"title": "AI regulation and enforcement brief", "age": "Live"},
            {"title": "Export control impact notes", "age": "Live"},
            {"title": "Public-sector AI adoption watch", "age": "Live"},
        ],
        "module_rows": [
            {"label": "Government Actions", "text": "Regulations, procurement rules, agency guidance, and public investment.", "status": "Live"},
            {"label": "Safety Institutes", "text": "Testing mandates, model evaluations, standards, and oversight bodies.", "status": "Tracking"},
            {"label": "Public Investment", "text": "Sovereign cloud, national compute, defense adoption, and public-sector pilots.", "status": "Watch"},
        ],
    },
    SectionVisualMode.MARKET_CHART: {
        "visual_class": "market-chart",
        "visual_label": "MARKET / CHART",
        "live_heading": "Capex Signals",
        "live_subheading": "AI infra index",
        "score_label": "Market relevance",
        "score_copy": "Tracking AI capex, cloud spending, semiconductor exposure, stocks, and valuation pressure.",
        "trending_heading": "Stock Watch",
        "trending_window": "24h",
        "watchlist_heading": "Market Snapshot",
        "watchlist_subheading": "AI exposure",
        "research_heading": "Spending Trends",
        "research_subheading": "Markets",
        "analysis_heading": "Valuation Pressure",
        "analysis_subheading": "Markets",
        "analysis_title": "Track the capex, valuation, stock, cloud-spend, and infrastructure investment signals.",
        "feed_kicker": "Markets Feed",
        "matched_heading": "Capital and market developments",
        "fallback_heading": "Latest market intelligence",
        "feature_label": "Market context",
        "active_status": "Market scan active",
        "fallback_status": "Markets fallback feed",
        "fallback_signals": [
            {"eyebrow": "Capex", "title": "AI infrastructure spending continues to set market expectations", "category": "Capex"},
            {"eyebrow": "Stocks", "title": "Semiconductor exposure drives strategic-technology baskets", "category": "Equities"},
            {"eyebrow": "Cloud", "title": "Cloud AI revenue becomes a key valuation signal", "category": "Spending"},
        ],
        "fallback_topics": [
            {"title": "AI capex cycle", "trend": "High"},
            {"title": "Semiconductor index pressure", "trend": "Rising"},
            {"title": "Cloud spending guidance", "trend": "Active"},
        ],
        "fallback_watchlist": [
            {"ticker": "AIQ", "value": "+2.1%", "class": "cx-positive"},
            {"ticker": "GPUX", "value": "+1.4%", "class": "cx-positive"},
            {"ticker": "CLD", "value": "-0.3%", "class": "cx-negative"},
        ],
        "fallback_briefs": [
            {"title": "AI capex and cloud-spending brief", "age": "Live"},
            {"title": "Semiconductor index exposure notes", "age": "Live"},
            {"title": "Valuation pressure and infrastructure demand watch", "age": "Live"},
        ],
        "module_rows": [
            {"label": "Market Snapshot", "text": "AI infrastructure exposure, semiconductor baskets, and cloud spending signals.", "status": "Live"},
            {"label": "Valuation Pressure", "text": "Earnings expectations, capex commitments, and multiples tied to AI demand.", "status": "Tracking"},
            {"label": "Spending Trends", "text": "Enterprise AI budgets, cloud commitments, and infrastructure investment cycles.", "status": "Watch"},
        ],
    },
    SectionVisualMode.RESEARCH_NETWORK: {
        "visual_class": "research-graph",
        "visual_label": "RESEARCH GRAPH",
        "live_heading": "Paper Signals",
        "live_subheading": "Benchmark watch",
        "score_label": "Research relevance",
        "score_copy": "Tracking papers, benchmarks, evaluations, model behavior, tool-use, and safety research.",
        "trending_heading": "Evaluation Notes",
        "trending_window": "24h",
        "watchlist_heading": "Model Evaluations",
        "watchlist_subheading": "Research layer",
        "research_heading": "Research Briefs",
        "research_subheading": "Papers",
        "analysis_heading": "Safety Findings",
        "analysis_subheading": "Research",
        "analysis_title": "Track papers, benchmarks, evaluations, reasoning, tool-use, and model behavior signals.",
        "feed_kicker": "Research Feed",
        "matched_heading": "Research and evaluation developments",
        "fallback_heading": "Latest research intelligence",
        "feature_label": "Research context",
        "active_status": "Research graph active",
        "fallback_status": "Research fallback feed",
        "fallback_signals": [
            {"eyebrow": "Papers", "title": "Reasoning evaluations put new pressure on benchmark design", "category": "Research"},
            {"eyebrow": "Tool-use", "title": "Agent benchmarks shift toward real task completion", "category": "Evaluation"},
            {"eyebrow": "Safety", "title": "Model behavior research tracks robustness under deployment", "category": "Safety"},
        ],
        "fallback_topics": [
            {"title": "Reasoning benchmarks", "trend": "High"},
            {"title": "Tool-use evaluation", "trend": "Rising"},
            {"title": "Model behavior safety", "trend": "Active"},
        ],
        "fallback_watchlist": [
            {"ticker": "EVAL", "value": "Bench", "class": ""},
            {"ticker": "RAG", "value": "Tool", "class": ""},
            {"ticker": "SAFE", "value": "Watch", "class": "cx-positive"},
        ],
        "fallback_briefs": [
            {"title": "Reasoning and long-context research brief", "age": "Live"},
            {"title": "Tool-use benchmark watch", "age": "Live"},
            {"title": "Model behavior and safety findings", "age": "Live"},
        ],
        "module_rows": [
            {"label": "Research Briefs", "text": "Papers, lab notes, benchmark releases, and frontier technical evidence.", "status": "Live"},
            {"label": "Model Evaluations", "text": "Reasoning, tool-use, long-context, robustness, and deployment benchmarks.", "status": "Tracking"},
            {"label": "Safety Findings", "text": "Behavior, alignment, reliability, and risk signals from applied research.", "status": "Watch"},
        ],
    },
}


class IntelligenceSectionPage(BasePage):
    template = "pages/intelligence_section_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    section_name = models.CharField(max_length=80, blank=True)
    section_label = models.CharField(max_length=120, blank=True)
    subtitle = models.TextField(blank=True)
    visual_mode = models.CharField(
        max_length=40,
        choices=SectionVisualMode.choices,
        default=SectionVisualMode.AI_CORE,
    )
    matching_terms = models.TextField(
        blank=True,
        help_text="Comma-separated matching terms used against article topic, context, title, intro, and signal tags.",
    )
    featured_article = models.ForeignKey(
        "news.ArticlePage",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional manual featured article. If empty, the latest matching article is used.",
    )
    signal_score = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Optional section score shown in the intelligence rail.",
    )
    section_cta_label = models.CharField(max_length=80, blank=True)
    section_cta_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional internal path or full URL.",
    )

    search_fields = BasePage.search_fields + [
        index.SearchField("section_name"),
        index.SearchField("section_label"),
        index.SearchField("subtitle"),
        index.SearchField("matching_terms"),
    ]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("section_name"),
                FieldPanel("section_label"),
                FieldPanel("subtitle"),
                FieldPanel("visual_mode"),
                FieldPanel("matching_terms"),
            ],
            heading="Section Identity",
        ),
        MultiFieldPanel(
            [
                FieldPanel("featured_article"),
                FieldPanel("signal_score"),
                FieldPanel("section_cta_label"),
                FieldPanel("section_cta_url"),
            ],
            heading="Curation",
        ),
        MultiFieldPanel(
            [
                InlinePanel("section_metrics", label="Section metrics"),
                InlinePanel("section_live_signals", label="Related live signals"),
                InlinePanel("section_trending_topics", label="Trending topics"),
                InlinePanel("section_research_briefs", label="Research briefs"),
                InlinePanel("section_watchlist_items", label="Market/watchlist items"),
            ],
            heading="Section Intelligence Modules",
        ),
    ]

    @property
    def matching_terms_list(self):
        raw_terms = self.matching_terms or self.slug.replace("-", " ")
        return [term.strip().lower() for term in raw_terms.split(",") if term.strip()]

    @property
    def display_section_name(self):
        return self.section_name or self.title

    @property
    def display_section_label(self):
        return self.section_label or f"{self.display_section_name} Intelligence"

    @property
    def cta_url(self):
        return self.section_cta_url or "/news/"

    @property
    def section_variant(self):
        return SECTION_VARIANTS.get(self.visual_mode, SECTION_VARIANTS[SectionVisualMode.AI_CORE])

    def get_matching_articles(self):
        queryset = (
            ArticlePage.objects.live()
            .public()
            .annotate(date=Coalesce("publication_date", "first_published_at"))
            .select_related("listing_image", "author", "topic")
            .order_by("-date")
        )
        query = Q()
        for term in self.matching_terms_list:
            query |= Q(topic__slug__icontains=term)
            query |= Q(topic__title__icontains=term)
            query |= Q(article_context_label__icontains=term)
            query |= Q(title__icontains=term)
            query |= Q(introduction__icontains=term)
            query |= Q(search_description__icontains=term)
            query |= Q(listing_title__icontains=term)
            query |= Q(listing_summary__icontains=term)
            query |= Q(intelligence_note__icontains=term)
            query |= Q(impact_model_title__icontains=term)
            query |= Q(impact_model_notes__icontains=term)
            query |= Q(signal_tags__label__icontains=term)
        if query:
            matched = queryset.filter(query).distinct()
            if matched.exists():
                return matched, False
        return queryset[:12], True

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        articles, is_fallback = self.get_matching_articles()
        articles = list(articles[:12])
        featured = None
        if self.featured_article and self.featured_article.live:
            featured = self.featured_article
        elif articles:
            featured = articles[0]

        context["section_articles"] = articles
        context["featured_article"] = featured
        context["section_is_fallback"] = is_fallback
        context["section_variant"] = self.section_variant
        context["configured_live_signals"] = [
            item.signal for item in self.section_live_signals.all() if item.signal
        ]
        context["configured_trending_topics"] = [
            item.topic for item in self.section_trending_topics.all() if item.topic
        ]
        context["configured_research_briefs"] = [
            item.brief for item in self.section_research_briefs.all() if item.brief
        ]
        context["configured_watchlist_items"] = [
            item.item for item in self.section_watchlist_items.all() if item.item
        ]
        return context


class SectionMetric(Orderable):
    page = ParentalKey(
        IntelligenceSectionPage,
        on_delete=models.CASCADE,
        related_name="section_metrics",
    )
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=40)
    status = models.CharField(max_length=40, blank=True)

    panels = [
        FieldPanel("label"),
        FieldPanel("value"),
        FieldPanel("status"),
    ]

    def __str__(self):
        return f"{self.value} {self.label}"


class SectionLiveSignal(Orderable):
    page = ParentalKey(
        IntelligenceSectionPage,
        on_delete=models.CASCADE,
        related_name="section_live_signals",
    )
    signal = models.ForeignKey(
        "intelligence.LiveSignal",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("signal")]


class SectionTrendingTopic(Orderable):
    page = ParentalKey(
        IntelligenceSectionPage,
        on_delete=models.CASCADE,
        related_name="section_trending_topics",
    )
    topic = models.ForeignKey(
        "intelligence.TrendingTopic",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("topic")]


class SectionResearchBrief(Orderable):
    page = ParentalKey(
        IntelligenceSectionPage,
        on_delete=models.CASCADE,
        related_name="section_research_briefs",
    )
    brief = models.ForeignKey(
        "intelligence.ResearchBrief",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("brief")]


class SectionWatchlistItem(Orderable):
    page = ParentalKey(
        IntelligenceSectionPage,
        on_delete=models.CASCADE,
        related_name="section_watchlist_items",
    )
    item = models.ForeignKey(
        "intelligence.MarketWatchlistItem",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("item")]
