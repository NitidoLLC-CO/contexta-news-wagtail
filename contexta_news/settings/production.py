from .base import *  # noqa

DEBUG = False

SERVE_MEDIA_WITH_DJANGO = (
    os.environ.get("SERVE_MEDIA_WITH_DJANGO", "true").lower()
    in {"1", "true", "yes", "on"}
)


# Security configuration

# Ensure that the session cookie is only sent by browsers under an HTTPS connection.
# https://docs.djangoproject.com/en/stable/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# Ensure that the CSRF cookie is only sent by browsers under an HTTPS connection.
# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# Allow the redirect importer to work in load-balanced / cloud environments.
# https://docs.wagtail.io/en/v2.13/reference/settings.html#redirects
WAGTAIL_REDIRECTS_FILE_STORAGE = "cache"

# Force HTTPS redirect (enabled by default!)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 31_536_000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "true").lower()
    in {"1", "true", "yes", "on"}
)
SECURE_HSTS_PRELOAD = (
    os.environ.get("SECURE_HSTS_PRELOAD", "true").lower()
    in {"1", "true", "yes", "on"}
)

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
