"""Админка orders с SMS при смене статуса."""
from django.contrib import admin

from .models import Order, OrderMessage


class OrderMessageInline(admin.TabularInline):
    """Чат заказа внутри админки."""

    model = OrderMessage
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админка заказов."""

    list_display = ('number', 'name', 'phone', 'service', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'service__category')
    search_fields = ('number', 'name', 'phone', 'email')
    readonly_fields = ('number', 'created_at', 'updated_at')
    list_editable = ('status',)
    inlines = [OrderMessageInline]
    date_hierarchy = 'created_at'
    actions = ('mark_in_progress', 'mark_done', 'mark_canceled')

    def save_model(self, request, obj, form, change):
        """Отправляет SMS при смене статуса через админку."""
        old_status = None
        if change and 'status' in form.changed_data:
            old_status = Order.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if old_status and old_status != obj.status:
            try:
                from apps.notifications.tasks import send_sms_order_status_changed
                send_sms_order_status_changed.delay(obj.pk, obj.status)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f'SMS Celery недоступен: {e}')

    @admin.action(description='В работу')
    def mark_in_progress(self, request, queryset):
        """Массово переводит в работу + SMS."""
        for order in queryset:
            old_status = order.status
            order.status = Order.Status.IN_PROGRESS
            order.save()
            if old_status != Order.Status.IN_PROGRESS:
                try:
                    from apps.notifications.tasks import send_sms_order_status_changed
                    send_sms_order_status_changed.delay(order.pk, order.status)
                except Exception:
                    pass

    @admin.action(description='Выполнено')
    def mark_done(self, request, queryset):
        """Массово помечает выполненными + SMS."""
        for order in queryset:
            old_status = order.status
            order.status = Order.Status.DONE
            order.save()
            if old_status != Order.Status.DONE:
                try:
                    from apps.notifications.tasks import send_sms_order_status_changed
                    send_sms_order_status_changed.delay(order.pk, order.status)
                except Exception:
                    pass

    @admin.action(description='Отменено')
    def mark_canceled(self, request, queryset):
        """Массово отменяет + SMS."""
        for order in queryset:
            old_status = order.status
            order.status = Order.Status.CANCELED
            order.save()
            if old_status != Order.Status.CANCELED:
                try:
                    from apps.notifications.tasks import send_sms_order_status_changed
                    send_sms_order_status_changed.delay(order.pk, order.status)
                except Exception:
                    pass


@admin.register(OrderMessage)
class OrderMessageAdmin(admin.ModelAdmin):
    """Админка сообщений."""

    list_display = ('order', 'sender', 'text', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('text', 'order__number')