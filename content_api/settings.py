"""
Django settings for content_api project.
"""

from pathlib import Path
import os
from datetime import timedelta

# ===============================
# BASE DIR
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# SECURITY
# ===============================
SECRET_KEY = 'django-insecure-5h3@p!oiyb8w=7w(sf-kc47_$7fa32y+&azgei+a9t@kyeuejz'
DEBUG = True
ALLOWED_HOSTS = ['*']


# ===============================
# NEXT.JS PROXY FIX (🔥 ВАЖНО 🔥)
# ===============================

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')


# ===============================
# APPLICATIONS
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'corsheaders',
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',

    # Local apps
    'content',
    'tests',
    'teacher_page',
    'home_page',
    'test_page',
    'faq',
    'vacancy',
    'authenticator',
    'contact',
    'coursepage',
    'blogs',
    'feedback',
    'bookpage',
]


# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',  # теперь БЕЗ редиректов
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===============================
# CORS
# ===============================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


# ===============================
# URLS / TEMPLATES
# ===============================
ROOT_URLCONF = 'content_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontenda/out'],  # Next.js build
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'content_api.wsgi.application'


# ===============================
# DATABASE
# ===============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ===============================
# REST FRAMEWORK
# ===============================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# ===============================
# JWT
# ===============================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}


# ===============================
# SWAGGER / SPECTACULAR
# ===============================
SPECTACULAR_SETTINGS = {
    'TITLE': 'English Test API',
    'DESCRIPTION': 'API для системы тестирования',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,

    'SECURITY': [
        {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    ],

    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'docExpansion': 'none',
        'deepLinking': True,
        'displayRequestDuration': True,
        'filter': True,
    },

    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',

    'ENUM_NAME_OVERRIDES': {
        'RoleEnum': 'authenticator.models.AdminUser.ROLE_CHOICES',
    },

    'PREPROCESSING_HOOKS': [
        'drf_spectacular.hooks.preprocess_exclude_path_format',
    ],
}


# ===============================
# PASSWORDS
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ===============================
# INTERNATIONALIZATION
# ===============================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ===============================
# STATIC / MEDIA
# ===============================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ===============================
# MODELS / SECURITY
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "authenticator.AdminUser"

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'