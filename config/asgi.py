"""
ASGI-конфигурация для проекта Service Hub.

Пригодится, если позже захотим WebSocket (чат в реальном времени).
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_asgi_application()
