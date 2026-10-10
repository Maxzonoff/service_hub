"""Модели masters: Master, MasterWork."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.services.models import Category


class Master(models.Model):
    """Исполнитель."""

    full_name = models.CharField(_('ФИО'), max_length=150)
    specialization = models.ManyToManyField(
        Category, related_name='masters', verbose_name=_('Специализация')
    )
    rating = models.DecimalField(_('Рейтинг'), max_digits=3, decimal_places=2, default=5.00)
    experience_years = models.PositiveSmallIntegerField(_('Опыт, лет'), default=1)
    photo = models.ImageField(_('Фото'), upload_to='masters/', blank=True, null=True)
    bio = models.TextField(_('О мастере'), blank=True)
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)

    class Meta:
        verbose_name = _('Мастер')
        verbose_name_plural = _('Мастера')
        ordering = ['-rating', 'full_name']

    def __str__(self):
        return f'{self.full_name} ({self.rating})'

    def get_absolute_url(self):
        """URL на мастера."""
        return reverse('masters:detail', kwargs={'pk': self.pk})


class MasterWork(models.Model):
    """Работа мастера (портфолио)."""

    master = models.ForeignKey(
        Master, on_delete=models.CASCADE, related_name='works', verbose_name=_('Мастер')
    )
    title = models.CharField(_('Название'), max_length=150)
    description = models.TextField(_('Описание'), blank=True)
    image = models.ImageField(_('Фото'), upload_to='portfolio/')
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)

    class Meta:
        verbose_name = _('Работа мастера')
        verbose_name_plural = _('Работы мастеров')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
