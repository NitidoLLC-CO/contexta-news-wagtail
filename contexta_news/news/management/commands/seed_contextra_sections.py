from django.core.management.base import BaseCommand

from contexta_news.home.models import HomePage
from contexta_news.intelligence.models import (
    LiveSignal,
    MarketWatchlistItem,
    ResearchBrief,
    TrendingTopic,
)
from contexta_news.news.models import (
    ArticlePage,
    IntelligenceSectionPage,
    SectionLiveSignal,
    SectionMetric,
    SectionResearchBrief,
    SectionTrendingTopic,
    SectionWatchlistItem,
)


SECTION_CONFIGS = [
    {
        "slug": "ai",
        "title": "AI",
        "section_name": "AI",
        "section_label": "AI INTELLIGENCE",
        "subtitle": "Tracking models, agents, infrastructure, safety, deployment, and the competitive systems defining AI.",
        "visual_mode": "ai-core",
        "matching_terms": "ai, artificial intelligence, model, models, agent, agents, reasoning, compute, frontier, benchmark, safety, deployment",
        "signal_score": "94.6",
        "metrics": [
            ("Model relevance", "94.6", "active"),
            ("Agentic watch", "Live", "active"),
            ("Benchmarks", "Tracking", "neutral"),
            ("Safety layer", "Active", "neutral"),
        ],
    },
    {
        "slug": "technology",
        "title": "Technology",
        "section_name": "Technology",
        "section_label": "TECHNOLOGY SIGNALS",
        "subtitle": "The chips, cloud, infrastructure, platforms, networks, and technical systems shaping the next operating layer.",
        "visual_mode": "chip-infrastructure",
        "matching_terms": "technology, chip, chips, semiconductor, hardware, gpu, cloud, compute, infrastructure, data center, datacenter, network, power",
        "signal_score": "92.4",
        "metrics": [
            ("Infrastructure relevance", "92.4", "active"),
            ("Chip signals", "Live", "active"),
            ("Cloud capacity", "Tight", "neutral"),
            ("Power demand", "Rising", "neutral"),
        ],
    },
    {
        "slug": "companies",
        "title": "Companies",
        "section_name": "Companies",
        "section_label": "COMPANY WATCH",
        "subtitle": "The firms, providers, labs, capital moves, partnerships, and strategic bets moving the intelligence economy.",
        "visual_mode": "company-cloud",
        "matching_terms": "company, companies, openai, anthropic, google, meta, microsoft, nvidia, oracle, xai, mistral, provider, lab, deal, partnership, funding",
        "signal_score": "90.8",
        "metrics": [
            ("Competitive relevance", "90.8", "active"),
            ("Provider watch", "Live", "active"),
            ("Deal flow", "Tracking", "neutral"),
            ("Lab pressure", "High", "neutral"),
        ],
    },
    {
        "slug": "policy",
        "title": "Policy",
        "section_name": "Policy",
        "section_label": "POLICY & POWER",
        "subtitle": "Where governance shapes tomorrow: regulation, trade, defense, institutions, and the power structures steering AI.",
        "visual_mode": "policy-government",
        "matching_terms": "policy, regulation, regulatory, government, governance, ai act, export, export control, law, safety institute, sovereignty, public sector, defense, power",
        "signal_score": "93.1",
        "metrics": [
            ("Policy relevance", "93.1", "active"),
            ("Regulation watch", "Live", "active"),
            ("Export controls", "Active", "neutral"),
            ("Sovereignty", "Rising", "neutral"),
        ],
    },
    {
        "slug": "markets",
        "title": "Markets",
        "section_name": "Markets",
        "section_label": "MARKET INTELLIGENCE",
        "subtitle": "Capital flows, sentiment, exposure, valuations, infrastructure demand, and market signals around AI and strategic technology.",
        "visual_mode": "market-chart",
        "matching_terms": "market, markets, finance, capital, capex, valuation, stock, spending, cloud spending, semiconductor index, investment, sentiment, revenue",
        "signal_score": "91.6",
        "metrics": [
            ("Market relevance", "91.6", "active"),
            ("Capex signals", "Live", "active"),
            ("AI infra index", "+2.1%", "neutral"),
            ("Valuation pressure", "High", "neutral"),
        ],
    },
    {
        "slug": "research",
        "title": "Research",
        "section_name": "Research",
        "section_label": "RESEARCH BRIEFING",
        "subtitle": "Signals from papers, labs, benchmarks, institutions, frontier technical research, and evidence shaping the field.",
        "visual_mode": "research-network",
        "matching_terms": "research, benchmark, benchmarks, paper, papers, evaluation, evaluations, model behavior, tool-use, tool use, safety research, long-context, reasoning, synthetic data, lab, evidence",
        "signal_score": "89.9",
        "metrics": [
            ("Research relevance", "89.9", "active"),
            ("Paper signals", "Live", "active"),
            ("Benchmark watch", "Tracking", "neutral"),
            ("Safety findings", "Active", "neutral"),
        ],
    },
]


def terms_for(config):
    return [term.strip().lower() for term in config["matching_terms"].split(",") if term.strip()]


def text_for(item, attrs):
    values = []
    for attr in attrs:
        value = getattr(item, attr, "")
        if callable(value):
            value = value()
        if value:
            values.append(str(value))
    return " ".join(values).lower()


def matched_items(items, config, attrs, limit=3):
    terms = terms_for(config)
    matches = []
    for item in items:
        text = text_for(item, attrs)
        score = sum(1 for term in terms if term in text)
        if score:
            matches.append((score, item))
    matches.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in matches[:limit]]


def matching_article(config):
    terms = terms_for(config)
    queryset = ArticlePage.objects.live().public().select_related("topic").order_by("-first_published_at")
    for article in queryset[:50]:
        text = " ".join(
            str(value)
            for value in [
                article.title,
                article.listing_title,
                article.listing_summary,
                article.search_description,
                article.introduction,
                article.article_context_label,
                article.topic.title if article.topic_id else "",
                article.topic.slug if article.topic_id else "",
            ]
            if value
        ).lower()
        if any(term in text for term in terms):
            return article
    return None


class Command(BaseCommand):
    help = "Create or update CONTEXTRA intelligence section pages without duplicates."

    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if home is None:
            self.stderr.write("No homepage exists. Cannot seed section pages.")
            return

        live_signals = list(LiveSignal.objects.active()[:24])
        trending_topics = list(TrendingTopic.objects.active()[:24])
        research_briefs = list(ResearchBrief.objects.active()[:24])
        watchlist_items = list(MarketWatchlistItem.objects.active()[:24])
        created_pages = 0
        updated_pages = 0

        for config in SECTION_CONFIGS:
            page = IntelligenceSectionPage.objects.filter(slug=config["slug"]).first()
            if page is None:
                page = IntelligenceSectionPage(title=config["title"], slug=config["slug"])
                home.add_child(instance=page)
                created_pages += 1
            else:
                updated_pages += 1

            page.title = config["title"]
            page.section_name = config["section_name"]
            page.section_label = config["section_label"]
            page.subtitle = config["subtitle"]
            page.visual_mode = config["visual_mode"]
            page.matching_terms = config["matching_terms"]
            page.signal_score = config["signal_score"]
            page.section_cta_label = f"Open {config['section_name']} brief"
            page.section_cta_url = "/news/"
            page.featured_article = matching_article(config)
            page.save()

            page.section_metrics.all().delete()
            page.section_live_signals.all().delete()
            page.section_trending_topics.all().delete()
            page.section_research_briefs.all().delete()
            page.section_watchlist_items.all().delete()

            metric_rows = config["metrics"]
            for index, (label, value, status) in enumerate(metric_rows):
                SectionMetric.objects.create(
                    page=page,
                    label=label,
                    value=value,
                    status=status,
                    sort_order=index,
                )

            section_live_signals = matched_items(
                live_signals,
                config,
                ["title", "category", "summary"],
            )
            section_trending_topics = matched_items(
                trending_topics,
                config,
                ["title", "category"],
            )
            section_research_briefs = matched_items(
                research_briefs,
                config,
                ["title", "summary", "category"],
            )
            section_watchlist_items = matched_items(
                watchlist_items,
                config,
                ["ticker", "company_name", "sector"],
            )

            for index, signal in enumerate(section_live_signals):
                SectionLiveSignal.objects.create(
                    page=page,
                    signal=signal,
                    sort_order=index,
                )
            for index, topic in enumerate(section_trending_topics):
                SectionTrendingTopic.objects.create(
                    page=page,
                    topic=topic,
                    sort_order=index,
                )
            for index, brief in enumerate(section_research_briefs):
                SectionResearchBrief.objects.create(
                    page=page,
                    brief=brief,
                    sort_order=index,
                )
            for index, item in enumerate(section_watchlist_items):
                SectionWatchlistItem.objects.create(
                    page=page,
                    item=item,
                    sort_order=index,
                )

            page.save_revision().publish()

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded CONTEXTRA sections (created={created_pages}, updated={updated_pages})."
            )
        )
