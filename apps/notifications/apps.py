"""Конфигурация приложения notifications."""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Настройки приложения notifications (email и SMS-уведомления)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notifications'
    verbose_name = 'Уведомления'
