"""Контекст-процессоры core."""

from .models import SiteSettings


def site_settings(request):
    """Передаёт настройки сайта во все шаблоны."""
    return {'site_settings': SiteSettings.load()}
