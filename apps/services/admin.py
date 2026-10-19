"""Админка приложения services."""
from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Service, ServiceImage


class ServiceImageInline(admin.TabularInline):
    """Inline галереи фото внутри карточки услуги."""

    model = ServiceImage
    extra = 1
    fields = ('image', 'thumbnail_preview', 'alt_text', 'order')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        """Миниатюра фото в админке."""
        if obj.pk and obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;">',
                obj.thumbnail.url,
            )
        return '—'

    thumbnail_preview.short_description = 'Превью'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка категорий."""

    list_display = ('name', 'slug', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Админка услуг."""

    list_display = ('name', 'category', 'price_from', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    list_select_related = ('category',)
    inlines = [ServiceImageInline]
    readonly_fields = ('image_preview',)

    fieldsets = (
        (None, {'fields': ('category', 'name', 'slug', 'is_active')}),
        ('Описание', {'fields': ('short_description', 'description')}),
        ('Цена и фото', {'fields': ('price_from', 'image', 'image_preview')}),
    )

    def image_preview(self, obj):
        """Превью главного фото."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:200px;border-radius:6px;">',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = 'Превью'


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    """Отдельная админка для фото услуг."""

    list_display = ('service', 'alt_text', 'order', 'created_at')
    list_filter = ('service',)
    list_editable = ('order',)