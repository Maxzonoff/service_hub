"""Админка портфолио."""
from django.contrib import admin
from django.utils.html import format_html

from .models import PortfolioImage, PortfolioWork


class PortfolioImageInline(admin.TabularInline):
    """Inline галереи внутри работы."""

    model = PortfolioImage
    extra = 1
    fields = ('image', 'thumbnail_preview', 'alt_text', 'order')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        """Превью."""
        if obj.pk and obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;">',
                obj.thumbnail.url,
            )
        return '—'

    thumbnail_preview.short_description = 'Превью'


@admin.register(PortfolioWork)
class PortfolioWorkAdmin(admin.ModelAdmin):
    """Админка работ."""

    list_display = ('title', 'category', 'main_image_preview', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PortfolioImageInline]
    readonly_fields = ('main_image_preview',)

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'category', 'is_active', 'order')}),
        ('Контент', {'fields': ('description', 'main_image', 'main_image_preview')}),
    )

    def main_image_preview(self, obj):
        """Превью главного фото."""
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-height:200px;border-radius:6px;">',
                obj.main_image.url,
            )
        return '—'

    main_image_preview.short_description = 'Превью'


@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    """Отдельная админка для фото работ."""

    list_display = ('work', 'alt_text', 'order', 'created_at')
    list_filter = ('work',)
    list_editable = ('order',)