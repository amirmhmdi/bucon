"""
Django settings for the BUCON project.

Stack: Django 4.2.x, django-allauth, django-crispy-forms + crispy-bootstrap5,
django-summernote, cloudinary storage, whitenoise, gunicorn,
dj-database-url + psycopg2.
"""

from pathlib import Path
from urllib.parse import unquote, urlparse

import dj_database_url
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # third-party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_summernote",
    "cloudinary_storage",
    "cloudinary",

    # local apps
    "accounts",
    "core",
    "blog",
    "portfolio",
    "timesheets",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "accounts.middleware.ForcePasswordChangeMiddleware",
]

ROOT_URLCONF = "config.urls"

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
                "core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

# django-allauth: no public signup — accounts are created by a manager/admin.
ACCOUNT_ADAPTER = "accounts.adapters.NoSignupAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = True

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "core:post_login_redirect"
ACCOUNT_LOGOUT_REDIRECT_URL = "core:home"


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
cloudinary_url = config("CLOUDINARY_URL", default="")
cloudinary_parts = urlparse(cloudinary_url) if cloudinary_url else None

if cloudinary_parts and cloudinary_parts.scheme == "cloudinary":
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": cloudinary_parts.hostname or "",
        "API_KEY": unquote(cloudinary_parts.username or ""),
        "API_SECRET": unquote(cloudinary_parts.password or ""),
    }
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
else:
    CLOUDINARY_STORAGE = {}
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

SUMMERNOTE_THEME = "bs5"

# URLs that don't require the forced-password-change redirect.
FORCE_PASSWORD_CHANGE_EXEMPT_URL_NAMES = [
    "accounts:force_password_change",
    "account_logout",
    "django_summernote-editor",
    "django_summernote-upload_attachment",
]
