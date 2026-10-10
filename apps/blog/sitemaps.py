"""Sitemap блога."""

from django.contrib.sitemaps import Sitemap

from .models import Post


class BlogSitemap(Sitemap):
    """Карта статей."""

    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        """Опубликованные статьи."""
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        """Дата публикации."""
        return obj.published_at
