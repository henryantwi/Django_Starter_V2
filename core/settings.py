from pathlib import Path
import dj_database_url
from email.utils import formataddr

from decouple import config, Csv
from django.urls import reverse_lazy

from icecream import ic

ic.disable()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

POSTGRES_LOCALLY = config("POSTGRES_LOCALLY", default=False, cast=bool)

ENVIRONMENT = config("ENVIRONMENT", default="production")

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS: list[str] = config("ENV_ALLOWED_HOSTS", cast=Csv())



INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cleanup.apps.CleanupConfig",
    "storages",
    "widget_tweaks",
    "django_htmx",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "a_home",
    "a_users",
]

SITE_ID = config("SITE_ID", default=1, cast=int)

SITE_NAME = config("SITE_NAME", default="Site Name")
SITE_DOMAIN = config("SITE_DOMAIN", default="site.domain")

PROJECT_NAME = config("PROJECT_NAME", default="Project Name")
PROJECT_DESCRIPTION = config("PROJECT_DESCRIPTION", default="Project Description")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "a_users.middleware.OnboardingMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if ENVIRONMENT == "production" or POSTGRES_LOCALLY is True:
    DATABASES["default"] = dj_database_url.parse(config("DATABASE_URL"))
    DATABASES["default"]["CONN_MAX_AGE"] = 600  # 10 minutes
    DATABASES["default"]["OPTIONS"] = {
        "sslmode": "require",
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Session Settings
if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "Lax"  # or 'None' if you need cross-site cookies
SESSION_COOKIE_NAME = "sessionid"  # Django's default, but being explicit
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 1209600  # 2 weeks, in seconds

# Security Settings

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"

SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_SIGNUP_REDIRECT_URL = reverse_lazy("profile-onboarding")
ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL = "/a_users/settings/"

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_EMAIL_SUBJECT_PREFIX = f"[{PROJECT_NAME}] "
# ACCOUNT_EMAIL_SUBJECT_PREFIX = config("ACCOUNT_EMAIL_SUBJECT_PREFIX", default="")
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""


# Social Account Settings
SOCIALACCOUNT_ADAPTER = "a_users.adapters.CustomSocialAccountAdapter"
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True


if DEBUG or POSTGRES_LOCALLY is True or ENVIRONMENT == "development":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
    EMAIL_TIMEOUT = 30
    EMAIL_SUBJECT_PREFIX = config("EMAIL_SUBJECT_PREFIX")
DEFAULT_FROM_EMAIL = formataddr((f"{PROJECT_NAME}", config("DEFAULT_FROM_EMAIL")))


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config("GOOGLE_CLIENT_ID"),
            "secret": config("GOOGLE_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
            "prompt": "select_account",
        },
    }
}

# Static files (CSS, JavaScript, Images)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles-cdn"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media/Static storage configuration: local for development, S3 for production
if DEBUG or ENVIRONMENT == "development":
    # Local storage for development
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    # Use S3/CDN config for production
    from .cdn.conf import *  # noqa
