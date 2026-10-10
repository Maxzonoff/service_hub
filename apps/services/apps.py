"""Конфигурация приложения services."""

from django.apps import AppConfig


class ServicesConfig(AppConfig):
    """Настройки приложения services (категории и услуги)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.services'
    verbose_name = 'Услуги'
