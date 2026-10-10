"""
Настройки для локальной разработки.

Наследуют base.py и включают:
- DEBUG=True
- django-debug-toolbar
- консольный email-backend (письма видны в терминале)
- отключённые throttling-механизмы для удобства
"""

from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ['*']

# Email → в консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CKEditor 5: в dev отключаем манифест whitenoise, чтобы файлы редактора грузились без хешей
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
# ─────────────────────────────────────────────
# Debug toolbar
# ─────────────────────────────────────────────
INSTALLED_APPS += ['debug_toolbar']  # noqa: F405

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405

INTERNAL_IPS = ['127.0.0.1', 'localhost']

# ─────────────────────────────────────────────
# Отключаем axes в dev (чтобы не блокироваться самому)
# ─────────────────────────────────────────────
AXES_ENABLED = False
