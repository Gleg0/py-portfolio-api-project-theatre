from config.settings.base import *  # noqa: F403,F405
from decouple import config

DEBUG = config("DEBUG", default=True, cast=bool)
SECRET_KEY = config("SECRET_KEY", default="dev-secret")
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

INSTALLED_APPS += ["django_extensions"]  # noqa: F403,F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}

REST_FRAMEWORK.update(
    {
        "DEFAULT_PAGINATION_CLASS": None,
        "DEFAULT_THROTTLE_CLASSES": [],
        "TEST_REQUEST_RENDERER_CLASSES": (
            "rest_framework.renderers.JSONRenderer",
        ),
    }
)

SPECTACULAR_SETTINGS["SERVE_INCLUDE_SCHEMA"] = False
