"""
Django settings for techsphere project.
"""

import os
from pathlib import Path

import dj_database_url
from decouple import config


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-local-dev-key",
)

DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool,
)

# Render / production
ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "ALLOWED_HOSTS",
        default="*",
    ).split(",")
    if host.strip()
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",

    # Cloudinary
    # Must come before django.contrib.staticfiles
    "cloudinary_storage",
    "django.contrib.staticfiles",
    "cloudinary",

    # Third-party
    "crispy_forms",
    "crispy_bootstrap5",
    "ckeditor",

    # Local apps
    "blog",
    "users",
]


# ============================================================
# CRISPY FORMS
# ============================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise for production static files
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "techsphere.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        # IMPORTANT:
        # The correct path is:
        # django.template.backends.django.DjangoTemplates
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # Your custom context processor
                "blog.context_processors.categories_processor",
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "techsphere.wsgi.application"


# ============================================================
# DATABASE
# ============================================================

# Production:
#   Render provides DATABASE_URL
#
# Local:
#   Falls back to SQLite

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

# Only use this directory if it exists
STATICFILES_DIRS = []

LOCAL_STATIC_DIR = BASE_DIR / "static"

if LOCAL_STATIC_DIR.exists():
    STATICFILES_DIRS.append(LOCAL_STATIC_DIR)


# WhiteNoise storage
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ============================================================
# MEDIA / CLOUDINARY
# ============================================================

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config(
        "CLOUDINARY_CLOUD_NAME",
        default="",
    ),
    "API_KEY": config(
        "CLOUDINARY_API_KEY",
        default="",
    ),
    "API_SECRET": config(
        "CLOUDINARY_API_SECRET",
        default="",
    ),
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# AUTHENTICATION
# ============================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "homepage"

LOGOUT_REDIRECT_URL = "homepage"


# ============================================================
# EMAIL
# ============================================================

# Local development:
# Emails appear in the terminal.

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)


# ============================================================
# CSRF / HTTPS
# ============================================================

# Add your Render URL through the environment variable:
#
# CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
#
# Multiple URLs can be separated by commas.

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config(
        "CSRF_TRUSTED_ORIGINS",
        default="",
    ).split(",")
    if origin.strip()
]


# Tell Django that Render's proxy is handling HTTPS
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
The critical fix
This is the line that was breaking your deployment:

"BACKEND": "django.template.backends.django.DjangoTemplates",
You had:

"BACKEND": "django.template.backends.DjangoTemplates",
The extra .django is essential.

One important Render setting
In your Render environment variables, make sure you have something like:

SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
And your Cloudinary variables:

CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
Render's PostgreSQL connection should provide:

DATABASE_URL=...