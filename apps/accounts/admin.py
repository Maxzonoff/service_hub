"""Админка accounts."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админка пользователей."""

    list_display = (
        'email',
        'first_name',
        'last_name',
        'phone',
        'is_master',
        'is_active',
        'created_at',
    )
    list_filter = ('is_master', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Личная информация'),
            {'fields': ('first_name', 'last_name', 'phone', 'address', 'avatar', 'is_master')},
        ),
        (
            _('Права'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')},
        ),
        (_('Даты'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'phone', 'first_name', 'password1', 'password2'),
            },
        ),
    )
