"""Конфигурация приложения masters."""

from django.apps import AppConfig


class MastersConfig(AppConfig):
    """Настройки приложения masters (исполнители и портфолио)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.masters'
    verbose_name = 'Мастера'
