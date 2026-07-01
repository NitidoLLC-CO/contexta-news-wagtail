from django import template

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

register = template.Library()


@register.simple_tag
def active_live_signals(limit=5):
    return list(
        LiveSignal.objects.active().order_by("sort_order", "-published_at", "id")[:limit]
    )


@register.simple_tag
def active_status_metrics(limit=5):
    return list(StatusMetric.objects.active().order_by("sort_order", "id")[:limit])


@register.simple_tag
def active_trending_topics(limit=5):
    return list(TrendingTopic.objects.active().order_by("sort_order", "id")[:limit])


@register.simple_tag
def active_model_tracker_items(limit=5):
    return list(AIModelTrackerItem.objects.active().order_by("sort_order", "id")[:limit])


@register.simple_tag
def active_watchlist_items(limit=5):
    return list(MarketWatchlistItem.objects.active().order_by("sort_order", "id")[:limit])


@register.simple_tag
def active_research_briefs(limit=3):
    return list(
        ResearchBrief.objects.active().order_by("sort_order", "-published_at", "id")[
            :limit
        ]
    )


@register.simple_tag
def active_north_signal_brief():
    return NorthSignalBrief.objects.filter(is_active=True).order_by("-updated_at", "id").first()


@register.simple_tag
def active_app_ecosystem_cta():
    return AppEcosystemCTA.objects.filter(is_active=True).order_by("-updated_at", "id").first()
