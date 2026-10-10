"""Модели core: SiteSettings, PromoCode, Advantage, FAQ, CallbackRequest."""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """Настройки сайта (singleton)."""

    site_name = models.CharField(_('Название сайта'), max_length=100, default='Service Hub')
    phone = models.CharField(_('Телефон'), max_length=20, default='+7 (999) 123-45-67')
    email = models.EmailField(_('Email'), default='info@servicehub.ru')
    address = models.CharField(_('Адрес'), max_length=255, blank=True)
    about_text = models.TextField(_('О нас'), blank=True)
    requisites = models.TextField(_('Реквизиты'), blank=True)
    telegram = models.URLField(_('Telegram'), blank=True)
    whatsapp = models.URLField(_('WhatsApp'), blank=True)
    vk = models.URLField(_('ВКонтакте'), blank=True)
    work_hours = models.CharField(_('Часы работы'), max_length=100, default='Ежедневно 8:00–22:00')
    guarantee_years = models.PositiveSmallIntegerField(_('Гарантия, лет'), default=3)
    response_minutes = models.PositiveSmallIntegerField(_('Мастер приедет через, мин'), default=30)

    class Meta:
        verbose_name = _('Настройки сайта')
        verbose_name_plural = _('Настройки сайта')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        """Singleton: только одна запись."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Возвращает единственный экземпляр."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Advantage(models.Model):
    """Преимущество для блока на главной."""

    title = models.CharField(_('Заголовок'), max_length=100)
    description = models.CharField(_('Описание'), max_length=255)
    icon = models.CharField(_('Иконка (Bootstrap Icons)'), max_length=50, default='bi-star')
    order = models.PositiveSmallIntegerField(_('Порядок'), default=0)
    is_active = models.BooleanField(_('Активно'), default=True)

    class Meta:
        verbose_name = _('Преимущество')
        verbose_name_plural = _('Преимущества')
        ordering = ['order']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    """Часто задаваемые вопросы."""

    question = models.CharField(_('Вопрос'), max_length=255)
    answer = models.TextField(_('Ответ'))
    order = models.PositiveSmallIntegerField(_('Порядок'), default=0)
    is_active = models.BooleanField(_('Активно'), default=True)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQ')
        ordering = ['order']

    def __str__(self):
        return self.question


class PromoCode(models.Model):
    """Промокод."""

    code = models.CharField(_('Код'), max_length=50, unique=True)
    discount_percent = models.PositiveSmallIntegerField(
        _('Скидка, %'),
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    valid_until = models.DateField(_('Действует до'), null=True, blank=True)
    is_active = models.BooleanField(_('Активен'), default=True)
    usage_limit = models.PositiveIntegerField(
        _('Лимит использований'), default=0, help_text='0 — без ограничений'
    )
    used_count = models.PositiveIntegerField(_('Использован раз'), default=0)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)

    class Meta:
        verbose_name = _('Промокод')
        verbose_name_plural = _('Промокоды')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.code} ({self.discount_percent}%)'

    def is_valid(self):
        """Проверяет, можно ли применить промокод."""
        if not self.is_active:
            return False
        if self.valid_until and self.valid_until < timezone.now().date():
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        return True


class CallbackRequest(models.Model):
    """Заявка на обратный звонок."""

    name = models.CharField(_('Имя'), max_length=100)
    phone = models.CharField(_('Телефон'), max_length=20)
    comment = models.TextField(_('Комментарий'), blank=True)
    is_processed = models.BooleanField(_('Обработана'), default=False)
    created_at = models.DateTimeField(_('Создана'), auto_now_add=True)

    class Meta:
        verbose_name = _('Обратный звонок')
        verbose_name_plural = _('Обратные звонки')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.phone}'
