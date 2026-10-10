"""Конфигурация приложения blog."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Настройки приложения blog (статьи для SEO)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'
    verbose_name = 'Блог'
