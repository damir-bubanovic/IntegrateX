import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root if present
load_dotenv(BASE_DIR / ".env")


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def _env_csv(name: str, default: list[str] | None = None) -> list[str]:
    val = os.getenv(name)
    if val is None:
        return default or []
    return [x.strip() for x in val.split(",") if x.strip()]


# Environment: dev | staging | prod
DJANGO_ENV = os.getenv("DJANGO_ENV", "dev").strip().lower()
if DJANGO_ENV not in {"dev", "staging", "prod"}:
    DJANGO_ENV = "dev"

# Secrets
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-change-me")
if DJANGO_ENV == "prod" and SECRET_KEY == "dev-insecure-change-me":
    raise RuntimeError(
        "Refusing to start with insecure DJANGO_SECRET_KEY in production. "
        "Set DJANGO_SECRET_KEY in your environment or .env."
    )

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Debug
# Default: True in dev, False otherwise; can be overridden by DJANGO_DEBUG
DEBUG = _env_bool("DJANGO_DEBUG", default=(DJANGO_ENV == "dev"))

# Allowed hosts
ALLOWED_HOSTS = _env_csv(
    "DJANGO_ALLOWED_HOSTS",
    default=["127.0.0.1", "localhost"] if DJANGO_ENV == "dev" else [],
)

# i18n/time
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# Apps
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "django_filters",
    "corsheaders",
    # Local
    "apps.users.apps.UsersConfig",
    "apps.organizations.apps.OrganizationsConfig",
    "apps.integrations.apps.IntegrationsConfig",
    "apps.notifications.apps.NotificationsConfig",
    "apps.audit.apps.AuditConfig",
]

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # API / production auth (preferred)
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # Browser / admin session support (dev-friendly)
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    # --- Rate limiting (Chapter 11.2) ---
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": os.getenv("DRF_THROTTLE_ANON", "100/day"),
        "user": os.getenv("DRF_THROTTLE_USER", "1000/day"),
        "burst": os.getenv("DRF_THROTTLE_BURST", "60/min"),
        "webhook": os.getenv("DRF_THROTTLE_WEBHOOK", "300/hour"),
    },
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.organizations.middleware.OrganizationMiddleware",
    "apps.audit.middleware.AuditMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS
# Dev default: allow all. In staging/prod, default to NOT allowing all.
CORS_ALLOW_ALL_ORIGINS = _env_bool(
    "CORS_ALLOW_ALL_ORIGINS",
    default=(DJANGO_ENV == "dev"),
)
CORS_ALLOWED_ORIGINS = _env_csv("CORS_ALLOWED_ORIGINS", default=[])

# Never allow '*' CORS outside dev
if DJANGO_ENV != "dev":
    CORS_ALLOW_ALL_ORIGINS = False

# CSRF
CSRF_TRUSTED_ORIGINS = _env_csv("CSRF_TRUSTED_ORIGINS", default=[])
CSRF_COOKIE_HTTPONLY = True

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# Static
STATIC_URL = "static/"
STATIC_ROOT = os.getenv("STATIC_ROOT", "staticfiles")

# Database
# Default remains sqlite3 with db.sqlite3 in project root.
DB_ENGINE = os.getenv("DB_ENGINE", "django.db.backends.sqlite3").strip()
DB_NAME = os.getenv("DB_NAME", "db.sqlite3").strip()

if DB_ENGINE == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / DB_NAME),
        }
    }
else:
    # postgres or other engines
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": os.getenv("DB_DATABASE", os.getenv("DB_NAME", "")),
            "USER": os.getenv("DB_USER", ""),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

# Production security toggles (minimal defaults)
if DJANGO_ENV == "prod":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = _env_bool("SECURE_SSL_REDIRECT", default=True)

    SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", default=True)
    CSRF_COOKIE_SECURE = _env_bool("CSRF_COOKIE_SECURE", default=True)

    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = _env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
    SECURE_HSTS_PRELOAD = _env_bool("SECURE_HSTS_PRELOAD", default=True)

    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# --- Celery / Redis ---
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = os.getenv("TIME_ZONE", "Europe/Zagreb")
CELERY_TASK_ALWAYS_EAGER = _env_bool("CELERY_TASK_ALWAYS_EAGER", default=False)  # helpful for tests/dev

# --- Email (dev defaults) ---
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@integratex.local")
