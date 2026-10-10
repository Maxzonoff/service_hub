"""
Корневая конфигурация URL проекта Service Hub.

Подключает:
- /admin/ — админка
- /ckeditor5/ — загрузка файлов из редактора
- /sitemap.xml, /robots.txt — SEO
- / — приложение core
- /services/, /orders/, /accounts/, /masters/, /reviews/, /blog/ — остальные приложения
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from apps.blog.sitemaps import BlogSitemap
from apps.core.sitemaps import StaticViewSitemap
from apps.services.sitemaps import ServiceSitemap

admin.site.site_header = 'Service Hub — Администрирование'
admin.site.site_title = 'Service Hub'
admin.site.index_title = 'Панель управления'

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'blog': BlogSitemap,
}

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
    path('masters/', include('apps.masters.urls', namespace='masters')),
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
