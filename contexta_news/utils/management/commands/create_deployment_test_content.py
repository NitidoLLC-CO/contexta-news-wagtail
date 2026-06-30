import base64

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from wagtail.models import Site

from contexta_news.home.models import HomePage
from contexta_news.images.models import CustomImage
from contexta_news.news.models import ArticlePage, NewsListingPage
from contexta_news.utils.models import ArticleTopic, AuthorSnippet


TEST_IMAGE_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+"
    "/p9sAAAAASUVORK5CYII="
)


class Command(BaseCommand):
    help = "Create minimal Railway deployment verification content."

    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if home is None:
            self.stderr.write("No homepage exists.")
            return

        author, _ = AuthorSnippet.objects.get_or_create(title="CONTEXTRA Editorial")
        topic, _ = ArticleTopic.objects.get_or_create(
            title="Deployment Test",
            defaults={"slug": "deployment-test"},
        )

        listing = NewsListingPage.objects.filter(slug="news").first()
        if listing is None:
            listing = NewsListingPage(
                title="News",
                slug="news",
                introduction="CONTEXTRA News",
            )
            home.add_child(instance=listing)
            listing.save_revision().publish()

        image = CustomImage.objects.filter(
            title="CONTEXTRA deployment test image"
        ).first()
        if image is None:
            image = CustomImage.objects.create(
                title="CONTEXTRA deployment test image",
                file=ContentFile(
                    base64.b64decode(TEST_IMAGE_BASE64),
                    name="deployment-test.png",
                ),
            )

        article = ArticlePage.objects.filter(slug="deployment-test-article").first()
        if article is None:
            article = ArticlePage(
                title="Deployment Test Article",
                slug="deployment-test-article",
                author=author,
                topic=topic,
                introduction="Railway deployment verification article.",
                body=[],
            )
            listing.add_child(instance=article)
        else:
            article.title = "Deployment Test Article"
            article.author = author
            article.topic = topic
            article.introduction = "Railway deployment verification article updated."

        article.listing_image = image
        article.save_revision().publish()

        site = Site.objects.get(is_default_site=True)
        self.stdout.write(f"site={site.site_name}")
        self.stdout.write(f"host={site.hostname}")
        self.stdout.write(f"listing_url={listing.relative_url(site)}")
        self.stdout.write(f"article_url={article.relative_url(site)}")
        self.stdout.write(f"image_url={image.file.url}")
