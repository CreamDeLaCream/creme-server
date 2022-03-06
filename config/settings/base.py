"""
environment variables:
    SECRET_KEY = "secret key"
    ALLOWED_HOSTS = https://aaa.com,https://bbb.com # 접속 허용할 hosts
"""

import json
import os
import sys
from datetime import timedelta
from pathlib import Path

from django.utils.translation import gettext_lazy as _

SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET KEY HERE")
# ------------------------------------------------
# 경로 설정
# ------------------------------------------------

# base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = Path(__file__).resolve().parent.parent

# static directory
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, ".static")

# media directory
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, ".media")

# secret key
SECRET_BASE_FILE = os.path.join(BASE_DIR, "secrets.json")
secrets = json.loads(open(SECRET_BASE_FILE).read())
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)


# 후행 슬래시 비활성화
APPEND_SLASH = False

# ------------------------------------------------
# 보안
# ------------------------------------------------

# Debug 기본값 False
DEBUG = False

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
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

# ------------------------------------------------
# 앱
# ------------------------------------------------

# django 앱
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# 써드파티 라이브러리
THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "silk",
    "drf_yasg",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]

# 프로젝트에서 생성한 앱
LOCAL_APPS = [
    "apps.core",
    "apps.users",
    "apps.analysis",
    "apps.dogs",
    "apps.questions",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


REST_FRAMEWORK = {
    # 인증 체계 설정
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
}

# TOKEN
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS512",
    "SIGNING_KEY": SECRET_KEY,
}


# ------------------------------------------------
# 미들웨어
# ------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
]

ROOT_URLCONF = "config.urls"

# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#overriding-admin-templates 참고
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "config.wsgi.application"


# ------------------------------------------------
# 데이터 베이스
# ------------------------------------------------
# AUTH_USER_MODEL ="<앱이름>.<유저모델이름>"
AUTH_USER_MODEL = "users.User"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# ------------------------------------------------
# I18n
# ------------------------------------------------

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("ko", _("Korean")),
]

LOCALE_PATHS = (os.path.join(CONFIG_DIR, "locale"),)

# ------------------------------------------------
# Thrid Party
# ------------------------------------------------
