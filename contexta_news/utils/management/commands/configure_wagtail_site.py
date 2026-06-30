import os
from urllib.parse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand
from wagtail.models import Site


def hostname_from_url(value):
    if not value:
        return None
    parsed = urlparse(value)
    return parsed.netloc or parsed.path.split("/")[0] or None


class Command(BaseCommand):
    help = "Configure the default Wagtail site from Railway/public environment variables."

    def handle(self, *args, **options):
        hostname = (
            os.environ.get("WAGTAIL_SITE_HOSTNAME")
            or os.environ.get("RAILWAY_PUBLIC_DOMAIN")
            or hostname_from_url(os.environ.get("WAGTAILADMIN_BASE_URL"))
            or "localhost"
        )

        site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        if site is None:
            self.stdout.write("No Wagtail site exists yet; skipping site configuration.")
            return

        site.hostname = hostname
        site.site_name = settings.WAGTAIL_SITE_NAME
        site.is_default_site = True
        site.save(update_fields=["hostname", "site_name", "is_default_site"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Configured Wagtail site '{settings.WAGTAIL_SITE_NAME}' at {hostname}."
            )
        )
