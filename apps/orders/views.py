"""
Представления приложения orders: создание заявки, просмотр, чат.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView, View

from apps.services.models import Service

from .forms import OrderForm
from .models import Order, OrderMessage


class OrderCreateView(View):
    """Онлайн-заявка на услугу."""

    def get(self, request):
        """Рендерит форму заявки."""
        initial = {}
        service_slug = request.GET.get('service')
        if service_slug:
            service = Service.objects.filter(slug=service_slug, is_active=True).first()
            if service:
                initial['service'] = service
        return render(request, 'orders/order_form.html', {'form': OrderForm(initial=initial)})

    def post(self, request):
        """Создаёт заказ и отправляет уведомления (email + SMS) через Celery."""
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.client = request.user
            order.save()

            # Email-уведомления
            try:
                from apps.notifications.tasks import notify_new_order
                notify_new_order.delay(order.pk)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f'Email Celery недоступен: {e}')

            # SMS-уведомления
            try:
                from apps.notifications.tasks import send_sms_order_created
                send_sms_order_created.delay(order.pk)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f'SMS Celery недоступен: {e}')

            messages.success(
                request,
                f'Заявка №{order.number} принята! Мы свяжемся с вами в течение 15 минут.',
            )
            return redirect('orders:success', number=order.number)
        return render(request, 'orders/order_form.html', {'form': form})


class OrderSuccessView(View):
    """Страница успешной заявки."""

    def get(self, request, number):
        """Показывает номер заказа."""
        order = get_object_or_404(Order, number=number)
        return render(request, 'orders/order_success.html', {'order': order})


class OrderDetailView(DetailView):
    """Просмотр заказа по номеру (для клиента)."""

    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        """Ищет заказ по номеру."""
        return get_object_or_404(Order, number=self.kwargs['number'])


@login_required
@require_GET
def order_messages(request, pk):
    """API: возвращает JSON со списком сообщений заказа."""
    order = get_object_or_404(Order, pk=pk)
    if order.client != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'forbidden'}, status=403)

    msgs = order.messages.select_related('sender').all()
    return JsonResponse({
        'messages': [
            {
                'id': m.pk,
                'text': m.text,
                'sender': m.sender.get_short_name(),
                'is_admin': m.is_admin_message,
                'created_at': m.created_at.strftime('%d.%m %H:%M'),
            }
            for m in msgs
        ]
    })


@login_required
@require_POST
def order_message_create(request, pk):
    """API: создаёт новое сообщение в чате заказа."""
    order = get_object_or_404(Order, pk=pk)
    if order.client != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'forbidden'}, status=403)

    text = (request.POST.get('text') or '').strip()
    if not text:
        return JsonResponse({'error': 'empty'}, status=400)

    msg = OrderMessage.objects.create(order=order, sender=request.user, text=text)
    return JsonResponse({
        'id': msg.pk,
        'text': msg.text,
        'created_at': msg.created_at.strftime('%d.%m %H:%M'),
    })