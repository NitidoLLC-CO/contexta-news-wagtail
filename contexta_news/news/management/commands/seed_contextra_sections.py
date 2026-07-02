from django.core.management.base import BaseCommand

from contexta_news.home.models import HomePage
from contexta_news.intelligence.models import (
    LiveSignal,
    MarketWatchlistItem,
    ResearchBrief,
    TrendingTopic,
)
from contexta_news.news.models import (
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
        "matching_terms": "ai, artificial intelligence, model, agent, compute, frontier, deployment",
        "signal_score": "94.6",
    },
    {
        "slug": "technology",
        "title": "Technology",
        "section_name": "Technology",
        "section_label": "TECHNOLOGY SIGNALS",
        "subtitle": "The chips, cloud, infrastructure, platforms, networks, and technical systems shaping the next operating layer.",
        "visual_mode": "chip-infrastructure",
        "matching_terms": "technology, chip, semiconductor, infrastructure, cloud, hardware, compute",
        "signal_score": "92.4",
    },
    {
        "slug": "companies",
        "title": "Companies",
        "section_name": "Companies",
        "section_label": "COMPANY WATCH",
        "subtitle": "The firms, providers, labs, capital moves, partnerships, and strategic bets moving the intelligence economy.",
        "visual_mode": "company-cloud",
        "matching_terms": "company, companies, openai, anthropic, google, microsoft, nvidia, provider, lab",
        "signal_score": "90.8",
    },
    {
        "slug": "policy",
        "title": "Policy",
        "section_name": "Policy",
        "section_label": "POLICY & POWER",
        "subtitle": "Where governance shapes tomorrow: regulation, trade, defense, institutions, and the power structures steering AI.",
        "visual_mode": "policy-government",
        "matching_terms": "policy, regulation, government, governance, ai act, export, law, power",
        "signal_score": "93.1",
    },
    {
        "slug": "markets",
        "title": "Markets",
        "section_name": "Markets",
        "section_label": "MARKET INTELLIGENCE",
        "subtitle": "Capital flows, sentiment, exposure, valuations, infrastructure demand, and market signals around AI and strategic technology.",
        "visual_mode": "market-chart",
        "matching_terms": "market, markets, finance, capital, valuation, stock, spending, sentiment",
        "signal_score": "91.6",
    },
    {
        "slug": "research",
        "title": "Research",
        "section_name": "Research",
        "section_label": "RESEARCH BRIEFING",
        "subtitle": "Signals from papers, labs, benchmarks, institutions, frontier technical research, and evidence shaping the field.",
        "visual_mode": "research-network",
        "matching_terms": "research, benchmark, paper, model robustness, synthetic data, lab, evidence",
        "signal_score": "89.9",
    },
]


class Command(BaseCommand):
    help = "Create or update CONTEXTRA intelligence section pages without duplicates."

    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if home is None:
            self.stderr.write("No homepage exists. Cannot seed section pages.")
            return

        live_signals = list(LiveSignal.objects.active()[:3])
        trending_topics = list(TrendingTopic.objects.active()[:3])
        research_briefs = list(ResearchBrief.objects.active()[:3])
        watchlist_items = list(MarketWatchlistItem.objects.active()[:3])
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
            page.save()

            metric_rows = [
                ("Section score", config["signal_score"], "active"),
                ("Signal mode", "Live", "active"),
                ("Coverage", "Global", "neutral"),
            ]
            for index, (label, value, status) in enumerate(metric_rows):
                SectionMetric.objects.update_or_create(
                    page=page,
                    label=label,
                    defaults={
                        "value": value,
                        "status": status,
                        "sort_order": index,
                    },
                )

            for index, signal in enumerate(live_signals):
                SectionLiveSignal.objects.get_or_create(
                    page=page,
                    signal=signal,
                    defaults={"sort_order": index},
                )
            for index, topic in enumerate(trending_topics):
                SectionTrendingTopic.objects.get_or_create(
                    page=page,
                    topic=topic,
                    defaults={"sort_order": index},
                )
            for index, brief in enumerate(research_briefs):
                SectionResearchBrief.objects.get_or_create(
                    page=page,
                    brief=brief,
                    defaults={"sort_order": index},
                )
            for index, item in enumerate(watchlist_items):
                SectionWatchlistItem.objects.get_or_create(
                    page=page,
                    item=item,
                    defaults={"sort_order": index},
                )

            page.save_revision().publish()

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded CONTEXTRA sections (created={created_pages}, updated={updated_pages})."
            )
        )
