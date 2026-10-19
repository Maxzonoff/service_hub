"""Конфигурация приложения portfolio."""
from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    """Настройки приложения portfolio (галерея работ)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.portfolio'
    verbose_name = 'Портфолио'