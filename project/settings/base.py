import os
import environ
from pathlib import Path
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured
# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Secret Key (يتم جلبه من .env)
SECRET_KEY = env('SECRET_KEY', default='your-secret-key')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',

    # My apps
    'accounts',
    'departments',
    'jobs',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'project.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI Application
WSGI_APPLICATION = 'project.wsgi.application'

# Authentication
AUTH_USER_MODEL = 'accounts.User'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT Authentication
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and Media files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# DRF Spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Workmate API',
    'DESCRIPTION': 'A comprehensive HR Management API.',
    'VERSION': '1.0.0',
}

ENV_FILE = os.path.join(Path(__file__).resolve().parent.parent.parent, '.env')
if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)  
else:
    raise ImproperlyConfigured("⚠ ملف .env غير موجود!")

# Email Settings
EMAIL_USER = env('EMAIL_USER', default=None)
EMAIL_PASS = env('EMAIL_PASS', default=None)

if not EMAIL_USER:
    raise ImproperlyConfigured("Set the EMAIL_USER environment variable")

if not EMAIL_PASS:
    raise ImproperlyConfigured("Set the EMAIL_PASS environment variable")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = EMAIL_USER
EMAIL_HOST_PASSWORD = EMAIL_PASS
DEFAULT_FROM_EMAIL = EMAIL_USER