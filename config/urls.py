"""
Корневая конфигурация URL проекта Service Hub.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from apps.blog.sitemaps import BlogSitemap
from apps.core.admin_dashboard import dashboard_context
from apps.core.sitemaps import StaticViewSitemap
from apps.services.sitemaps import ServiceSitemap

# ─────────────────────────────────────────────
# Заголовки админки
# ─────────────────────────────────────────────
admin.site.site_header = 'Service Hub — Администрирование'
admin.site.site_title = 'Service Hub'
admin.site.index_title = 'Панель управления'

# ─────────────────────────────────────────────
# Подключаем кастомный дашборд
# ─────────────────────────────────────────────
admin.site.index_template = 'admin/index.html'

_original_each_context = admin.site.each_context


def _patched_each_context(request):
    """Дополняет контекст админки метриками дашборда."""
    ctx = _original_each_context(request)
    ctx.update(dashboard_context(request))
    return ctx


admin.site.each_context = _patched_each_context

# ─────────────────────────────────────────────
# Sitemap
# ─────────────────────────────────────────────
sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'blog': BlogSitemap,
}

# ─────────────────────────────────────────────
# URL-маршруты
# ─────────────────────────────────────────────
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots',
    ),
    path('', include('apps.core.urls', namespace='core')),
    path('services/', include('apps.services.urls', namespace='services')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('reviews/', include('apps.reviews.urls', namespace='reviews')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    try:
        import debug_toolbar  # noqa: F401
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    except ImportError:
        pass