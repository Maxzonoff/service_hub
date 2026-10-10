"""Модели reviews: Review."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    """Отзыв клиента."""

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name=_('Клиент'),
    )
    name = models.CharField(_('Имя'), max_length=100)
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name=_('Заказ'),
    )
    rating = models.PositiveSmallIntegerField(
        _('Оценка'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField(_('Текст отзыва'))
    is_published = models.BooleanField(_('Опубликован'), default=False)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.rating}★'
