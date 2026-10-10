"""Sitemap для статических страниц."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Карта статических страниц."""

    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        """Список имён URL."""
        return [
            'core:home',
            'core:about',
            'core:contacts',
            'services:list',
            'blog:list',
            'reviews:list',
        ]

    def location(self, item):
        """Возвращает URL."""
        return reverse(item)
