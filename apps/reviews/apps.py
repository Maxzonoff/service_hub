"""Конфигурация приложения reviews."""

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Настройки приложения reviews (отзывы с модерацией)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reviews'
    verbose_name = 'Отзывы'
