"""Админка masters."""

from django.contrib import admin

from .models import Master, MasterWork


class MasterWorkInline(admin.TabularInline):
    """Работы внутри карточки мастера."""

    model = MasterWork
    extra = 0


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    """Админка мастеров."""

    list_display = ('full_name', 'rating', 'experience_years', 'is_active')
    list_filter = ('is_active', 'specialization')
    search_fields = ('full_name',)
    filter_horizontal = ('specialization',)
    inlines = [MasterWorkInline]


@admin.register(MasterWork)
class MasterWorkAdmin(admin.ModelAdmin):
    """Админка работ."""

    list_display = ('title', 'master', 'created_at')
    list_filter = ('master',)
