"""Модель пользователя."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


def user_avatar_path(instance, filename):
    """Путь для загрузки аватара."""
    return f'avatars/user_{instance.pk or "new"}/{filename}'


class User(AbstractUser):
    """Кастомный пользователь: email вместо username, поля phone, avatar, address."""

    username = None
    first_name = models.CharField(_('Имя'), max_length=100)
    last_name = models.CharField(_('Фамилия'), max_length=100, blank=True)

    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(_('Телефон'), max_length=20, unique=True)
    avatar = models.ImageField(_('Аватар'), upload_to=user_avatar_path, blank=True, null=True)
    address = models.CharField(_('Адрес'), max_length=255, blank=True)
    is_master = models.BooleanField(_('Исполнитель'), default=False)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлён'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    def get_short_name(self):
        """Имя для шаблонов."""
        return self.first_name or self.email.split('@')[0]

    def get_full_name(self):
        """Полное имя."""
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    def get_absolute_url(self):
        """URL на профиль."""
        return reverse('accounts:profile')
