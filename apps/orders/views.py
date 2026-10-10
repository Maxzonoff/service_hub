"""Представления orders."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View

from apps.services.models import Service

from .forms import OrderForm
from .models import Order


class OrderCreateView(View):
    """Онлайн-заявка."""

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
        """Создаёт заказ и отправляет уведомления через Celery."""
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.client = request.user
            order.save()

            # Celery-задачи уведомлений (в dev — просто в консоль)
            try:
                from apps.notifications.tasks import notify_new_order

                notify_new_order.delay(order.pk)
            except Exception as e:
                import logging

                logging.getLogger(__name__).warning(f'Celery недоступен: {e}')

            messages.success(
                request, f'Заявка №{order.number} принята! Мы свяжемся с вами в течение 15 минут.'
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
    slug_url_kwarg = 'number'

    def get_object(self, queryset=None):
        """Ищет заказ по номеру."""
        return get_object_or_404(Order, number=self.kwargs['number'])
