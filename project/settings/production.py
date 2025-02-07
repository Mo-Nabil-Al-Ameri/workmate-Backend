from .base import *

# Debug Mode (يجب أن يكون False في الإنتاج)
DEBUG = False

# Allowed Hosts (يتم قراءتها من .env)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Database (PostgreSQL)
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
