"""Sitemap для услуг."""

from django.contrib.sitemaps import Sitemap

from .models import Service, Category


class ServiceSitemap(Sitemap):
    """Карта услуг."""

    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        """Список активных услуг."""
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        """Дата последнего изменения."""
        return obj.created_at
