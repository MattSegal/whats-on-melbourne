from . import *

DEBUG = False
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = [
    "167.99.78.141",
    "127.0.0.1",
    "localhost",
    "whatsonmelb.fun",
    "www.whatsonmelb.fun",
    "api.whatsonmelb.fun",
]

SESSION_COOKIE_DOMAIN = ".whatsonmelb.fun"
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_DOMAIN = ".whatsonmelb.fun"
CSRF_TRUSTED_ORIGINS = [".whatsonmelb.fun"]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = (
    r"^(https?://)?(\w*-*\w*\.+)*whatsonmelb\.fun$",
    r"^(https?://)?(localhost|127\.0\.0\.1|0\.0\.0\.0)(:\d{4})?$",
)

# Get DRF to use HTTPS in links.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Logging
LOGGING["root"]["handlers"] = ["console", "sentry"]
LOGGING["handlers"]["sentry"] = {
    "level": "ERROR",
    "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
}

RAVEN_CONFIG = {"dsn": os.environ.get("RAVEN_DSN")}
