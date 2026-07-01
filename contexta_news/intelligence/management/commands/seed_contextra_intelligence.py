from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from contexta_news.intelligence.models import (
    AIModelTrackerItem,
    AppEcosystemCTA,
    LiveSignal,
    MarketWatchlistItem,
    NorthSignalBrief,
    ResearchBrief,
    StatusMetric,
    TrendingTopic,
)


class Command(BaseCommand):
    help = "Seed initial CONTEXTRA intelligence snippets without creating duplicates."

    def handle(self, *args, **options):
        now = timezone.now()
        created = {}

        if not LiveSignal.objects.exists():
            LiveSignal.objects.bulk_create(
                [
                    LiveSignal(
                        title="OpenAI expands model context window to 2M tokens",
                        category="AI Infrastructure",
                        published_at=now - timedelta(minutes=2),
                        impact_level="high",
                        summary="Frontier model context limits continue moving upward for enterprise research and agent workflows.",
                        sort_order=10,
                    ),
                    LiveSignal(
                        title="EU AI Act implementation guidelines published",
                        category="Policy & Regulation",
                        published_at=now - timedelta(minutes=15),
                        impact_level="high",
                        summary="Regulatory guidance clarifies obligations for high-risk AI systems and foundation model providers.",
                        sort_order=20,
                    ),
                    LiveSignal(
                        title="Global GPU supply tightens as demand accelerates",
                        category="AI Infrastructure",
                        published_at=now - timedelta(minutes=28),
                        impact_level="critical",
                        summary="Cloud and sovereign buyers compete for constrained accelerator capacity.",
                        sort_order=30,
                    ),
                    LiveSignal(
                        title="India launches national compute initiative",
                        category="Global Policy",
                        published_at=now - timedelta(minutes=45),
                        impact_level="medium",
                        summary="Public compute investment expands regional AI capacity and model-development access.",
                        sort_order=40,
                    ),
                ]
            )
            created["Live signals"] = 4

        if not StatusMetric.objects.exists():
            StatusMetric.objects.bulk_create(
                [
                    StatusMetric(
                        label="North Signal Status",
                        value="Active",
                        status="active",
                        sort_order=10,
                    ),
                    StatusMetric(
                        label="Systems Monitoring",
                        value="98.7%",
                        sublabel="Operational",
                        status="neutral",
                        sort_order=20,
                    ),
                    StatusMetric(
                        label="Signals Today",
                        value="1,248",
                        sublabel="Global scan",
                        status="active",
                        sort_order=30,
                    ),
                    StatusMetric(
                        label="Market Sentiment",
                        value="Bullish",
                        sparkline="+2.4",
                        status="bullish",
                        sort_order=40,
                    ),
                    StatusMetric(
                        label="Global Coverage",
                        value="87 Countries",
                        status="neutral",
                        sort_order=50,
                    ),
                ]
            )
            created["Status metrics"] = 5

        if not TrendingTopic.objects.exists():
            TrendingTopic.objects.bulk_create(
                [
                    TrendingTopic(
                        title="AI Compute Sovereignty",
                        category="Policy",
                        signal_count=184,
                        trend_label="high",
                        sort_order=10,
                    ),
                    TrendingTopic(
                        title="Agentic AI Platforms",
                        category="Models",
                        signal_count=163,
                        trend_label="high",
                        sort_order=20,
                    ),
                    TrendingTopic(
                        title="Energy for AI Infrastructure",
                        category="Infrastructure",
                        signal_count=121,
                        trend_label="medium",
                        sort_order=30,
                    ),
                    TrendingTopic(
                        title="Robotics & Physical AI",
                        category="Technology",
                        signal_count=97,
                        trend_label="medium",
                        sort_order=40,
                    ),
                    TrendingTopic(
                        title="Synthetic Data",
                        category="Research",
                        signal_count=88,
                        trend_label="rising",
                        sort_order=50,
                    ),
                ]
            )
            created["Trending topics"] = 5

        if not AIModelTrackerItem.objects.exists():
            AIModelTrackerItem.objects.bulk_create(
                [
                    AIModelTrackerItem(
                        model_name="OpenAI GPT-5",
                        provider="OpenAI",
                        score="95.2",
                        delta="+2.1",
                        status="Frontier",
                        icon_label="OAI",
                        sort_order=10,
                    ),
                    AIModelTrackerItem(
                        model_name="Claude 4 Opus",
                        provider="Anthropic",
                        score="93.7",
                        delta="+1.8",
                        status="Frontier",
                        icon_label="ANT",
                        sort_order=20,
                    ),
                    AIModelTrackerItem(
                        model_name="Gemini 2.5 Pro",
                        provider="Google DeepMind",
                        score="92.1",
                        delta="+1.2",
                        status="Advanced",
                        icon_label="GDM",
                        sort_order=30,
                    ),
                    AIModelTrackerItem(
                        model_name="Llama 4 Maverick",
                        provider="Meta",
                        score="90.3",
                        delta="+0.9",
                        status="Open weights",
                        icon_label="META",
                        sort_order=40,
                    ),
                    AIModelTrackerItem(
                        model_name="Qwen 2.5 Max",
                        provider="Alibaba",
                        score="88.6",
                        delta="+0.7",
                        status="Enterprise",
                        icon_label="QW",
                        sort_order=50,
                    ),
                ]
            )
            created["AI model tracker items"] = 5

        if not MarketWatchlistItem.objects.exists():
            MarketWatchlistItem.objects.bulk_create(
                [
                    MarketWatchlistItem(
                        ticker="NVDA",
                        company_name="NVIDIA Corporation",
                        delta="+3.4%",
                        delta_direction="up",
                        sector="AI chips",
                        sort_order=10,
                    ),
                    MarketWatchlistItem(
                        ticker="MSFT",
                        company_name="Microsoft Corporation",
                        delta="+1.1%",
                        delta_direction="up",
                        sector="Cloud AI",
                        sort_order=20,
                    ),
                    MarketWatchlistItem(
                        ticker="GOOGL",
                        company_name="Alphabet Inc.",
                        delta="+2.14%",
                        delta_direction="up",
                        sector="Models",
                        sort_order=30,
                    ),
                    MarketWatchlistItem(
                        ticker="AVGO",
                        company_name="Broadcom Inc.",
                        delta="-0.8%",
                        delta_direction="down",
                        sector="Semiconductors",
                        sort_order=40,
                    ),
                    MarketWatchlistItem(
                        ticker="TSM",
                        company_name="Taiwan Semiconductor",
                        delta="+1.06%",
                        delta_direction="up",
                        sector="Foundry",
                        sort_order=50,
                    ),
                ]
            )
            created["Market/watchlist items"] = 5

        if not ResearchBrief.objects.exists():
            ResearchBrief.objects.bulk_create(
                [
                    ResearchBrief(
                        title="Compute Access Inequality",
                        summary="How constrained accelerator access reshapes competition between labs, startups, and sovereign AI programs.",
                        category="Infrastructure",
                        document_type="briefing",
                        published_at=now - timedelta(hours=2),
                        sort_order=10,
                    ),
                    ResearchBrief(
                        title="Model Robustness Benchmark",
                        summary="A briefing on benchmark drift, adversarial pressure, and frontier model reliability.",
                        category="Research",
                        document_type="research",
                        published_at=now - timedelta(hours=4),
                        sort_order=20,
                    ),
                    ResearchBrief(
                        title="AI & Labor Market Impact",
                        summary="Signals from enterprise deployment, workforce redesign, and policy response.",
                        category="Markets",
                        document_type="report",
                        published_at=now - timedelta(hours=6),
                        sort_order=30,
                    ),
                ]
            )
            created["Research briefs"] = 3

        if not NorthSignalBrief.objects.exists():
            NorthSignalBrief.objects.create(
                title="Daily intelligence delivered",
                subtitle="North Signal Brief",
                body="The essential morning brief for AI, markets, policy, and power.",
                cta_label="Preview brief",
                cta_url="/news/",
                email_placeholder="Enter your email",
                trust_text="Trusted by 45,000+ professionals",
            )
            created["North Signal briefs"] = 1

        if not AppEcosystemCTA.objects.exists():
            AppEcosystemCTA.objects.create(
                title="Intelligence. Anywhere.",
                subtitle="North Signal App",
                body="Access real-time signals, expert analysis, and personalized intelligence on the go.",
                cta_label="Explore the app",
                cta_url="/news/",
            )
            created["App/ecosystem CTAs"] = 1

        if created:
            for label, count in created.items():
                self.stdout.write(self.style.SUCCESS(f"Created {count} {label}."))
        else:
            self.stdout.write("CONTEXTRA intelligence snippets already exist. No changes made.")
