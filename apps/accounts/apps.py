"""Конфигурация приложения accounts."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Настройки приложения accounts (пользователи, регистрация, профиль)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Пользователи'
