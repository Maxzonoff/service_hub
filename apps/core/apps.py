"""Конфигурация приложения core."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Настройки приложения core (главная, о нас, контакты, SEO)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Основное'
