from .base import *

# Debug Mode
DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.172.163']

# Database (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS Headers (للتعامل مع Flutter أثناء التطوير)
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOW_ALL_ORIGINS = True