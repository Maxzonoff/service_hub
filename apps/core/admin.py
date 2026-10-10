"""Админка core."""

from django.contrib import admin

from .models import Advantage, CallbackRequest, FAQ, PromoCode, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Настройки сайта."""

    def has_add_permission(self, request):
        """Запрещает создавать больше одной записи."""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Запрещает удалять настройки."""
        return False


@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    """Админка преимуществ."""

    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Админка FAQ."""

    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    """Админка промокодов."""

    list_display = (
        'code',
        'discount_percent',
        'valid_until',
        'is_active',
        'used_count',
        'usage_limit',
    )
    list_filter = ('is_active', 'valid_until')
    search_fields = ('code',)


@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    """Админка обратных звонков."""

    list_display = ('name', 'phone', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'phone')
    actions = ('mark_processed',)

    @admin.action(description='Отметить как обработанные')
    def mark_processed(self, request, queryset):
        """Массово помечает обработанными."""
        queryset.update(is_processed=True)
