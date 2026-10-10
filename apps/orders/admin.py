"""Админка orders."""

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

    @admin.action(description='В работу')
    def mark_in_progress(self, request, queryset):
        """Массово переводит в работу."""
        queryset.update(status=Order.Status.IN_PROGRESS)

    @admin.action(description='Выполнено')
    def mark_done(self, request, queryset):
        """Массово помечает выполненными."""
        queryset.update(status=Order.Status.DONE)

    @admin.action(description='Отменено')
    def mark_canceled(self, request, queryset):
        """Массово отменяет."""
        queryset.update(status=Order.Status.CANCELED)


@admin.register(OrderMessage)
class OrderMessageAdmin(admin.ModelAdmin):
    """Админка сообщений."""

    list_display = ('order', 'sender', 'text', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('text', 'order__number')
