"""Модели services: Category, Service."""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Категория услуг."""

    name = models.CharField(_('Название'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=120, unique=True, blank=True)
    icon = models.CharField(_('Иконка (Bootstrap Icons)'), max_length=50, default='bi-tools')
    description = models.TextField(_('Описание'), blank=True)
    order = models.PositiveSmallIntegerField(_('Порядок'), default=0)
    is_active = models.BooleanField(_('Активна'), default=True)

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Автогенерация slug."""
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL на категорию."""
        return reverse('services:category', kwargs={'slug': self.slug})


class Service(models.Model):
    """Услуга."""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='services', verbose_name=_('Категория')
    )
    name = models.CharField(_('Название'), max_length=150)
    slug = models.SlugField(_('Slug'), max_length=170, unique=True, blank=True)
    short_description = models.CharField(_('Краткое описание'), max_length=255, blank=True)
    description = models.TextField(_('Полное описание'), blank=True)
    price_from = models.DecimalField(_('Цена от, ₽'), max_digits=10, decimal_places=2)
    image = models.ImageField(_('Изображение'), upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(_('Создана'), auto_now_add=True)

    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.category.name} → {self.name}'

    def save(self, *args, **kwargs):
        """Автогенерация slug."""
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL на услугу."""
        return reverse('services:detail', kwargs={'slug': self.slug})
