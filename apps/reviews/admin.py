"""Админка reviews."""

from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка отзывов."""

    list_display = ('name', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating', 'created_at')
    search_fields = ('name', 'text')
    list_editable = ('is_published',)
    actions = ('publish', 'unpublish')

    @admin.action(description='Опубликовать')
    def publish(self, request, queryset):
        """Публикует выбранные отзывы."""
        queryset.update(is_published=True)

    @admin.action(description='Снять с публикации')
    def unpublish(self, request, queryset):
        """Снимает с публикации."""
        queryset.update(is_published=False)
