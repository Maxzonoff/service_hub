"""
Настройки для production.

Наследуют base.py и включают:
- DEBUG=False
- безопасные cookies, HSTS, SSL-редирект
- whitenoise для сжатой статики
- логирование в файлы
"""

from .base import *  # noqa: F401, F403

DEBUG = False

# ─────────────────────────────────────────────
# Безопасность
# ─────────────────────────────────────────────
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)  # noqa: F405
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)  # noqa: F405
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)  # noqa: F405
SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ─────────────────────────────────────────────
# Статика — сжатие через whitenoise
# ─────────────────────────────────────────────
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─────────────────────────────────────────────
# Логирование — только в файлы
# ─────────────────────────────────────────────
LOGGING['handlers']['console']['level'] = 'WARNING'  # noqa: F405
