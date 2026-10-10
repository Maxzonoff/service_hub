"""Модели orders: Order, OrderMessage."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """Заказ на услугу."""

    class Status(models.TextChoices):
        """Статусы заказа."""

        NEW = 'new', _('Новый')
        IN_PROGRESS = 'in_progress', _('В работе')
        DONE = 'done', _('Выполнен')
        CANCELED = 'canceled', _('Отменён')

    number = models.CharField(_('Номер'), max_length=20, unique=True, blank=True)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name=_('Клиент'),
    )
    name = models.CharField(_('Имя'), max_length=100)
    phone = models.CharField(_('Телефон'), max_length=20)
    email = models.EmailField(_('Email'), blank=True)
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name=_('Услуга'),
    )
    address = models.CharField(_('Адрес'), max_length=255)
    preferred_date = models.DateField(_('Желаемая дата'), null=True, blank=True)
    comment = models.TextField(_('Комментарий'), blank=True)
    status = models.CharField(
        _('Статус'), max_length=20, choices=Status.choices, default=Status.NEW
    )
    promo_code = models.ForeignKey(
        'core.PromoCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Промокод'),
    )
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлён'), auto_now=True)

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        ordering = ['-created_at']

    def __str__(self):
        return f'№{self.number} — {self.name} ({self.get_status_display()})'

    def save(self, *args, **kwargs):
        """Автогенерация номера заказа."""
        if not self.number:
            today = timezone.now()
            prefix = f'SH-{today.strftime("%Y%m%d")}'
            count = Order.objects.filter(number__startswith=prefix).count() + 1
            self.number = f'{prefix}-{count:04d}'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL на заказ (для админа)."""
        return reverse('orders:detail', kwargs={'number': self.number})


class OrderMessage(models.Model):
    """Сообщение в чате заказа."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='messages', verbose_name=_('Заказ')
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order_messages',
        verbose_name=_('Отправитель'),
    )
    text = models.TextField(_('Текст'))
    is_read = models.BooleanField(_('Прочитано'), default=False)
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)

    class Meta:
        verbose_name = _('Сообщение')
        verbose_name_plural = _('Сообщения')
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} @ {self.created_at:%H:%M}'

    @property
    def is_admin_message(self):
        """Сообщение от админа."""
        return self.sender.is_staff
