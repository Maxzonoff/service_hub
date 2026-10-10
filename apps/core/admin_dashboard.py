"""
Дашборд админки: собирает метрики для главной страницы /admin/.

Подключается через переопределение admin.site.each_context в config/urls.py.
"""
from django.db.models import Count
from django.utils import timezone

from apps.core.models import CallbackRequest
from apps.orders.models import Order
from apps.reviews.models import Review


def dashboard_context(request):
    """
    Собирает метрики для дашборда админки.

    Args:
        request: HTTP-запрос.

    Returns:
        dict: словарь с метриками и списками для шаблона admin/index.html.
    """
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    return {
        'orders_this_month': Order.objects.filter(created_at__gte=month_start).count(),
        'orders_done': Order.objects.filter(status=Order.Status.DONE).count(),
        'orders_new': Order.objects.filter(status=Order.Status.NEW).count(),
        'callbacks_pending': CallbackRequest.objects.filter(is_processed=False).count(),
        'reviews_pending': Review.objects.filter(is_published=False).count(),
        'top_services': (
            Order.objects
            .values('service__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        ),
        'recent_orders': Order.objects.order_by('-created_at')[:5],
    }