"""
Модели приложения services: Category, Service, ServiceImage.
"""
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image


# ─────────────────────────────────────────────
# Вспомогательные функции
# ─────────────────────────────────────────────
def _resize_image(image_field, max_width=1600, max_height=1600, quality=85):
    """
    Уменьшает загруженное изображение до указанных размеров.

    Args:
        image_field: Django ImageField (уже с файлом).
        max_width: максимальная ширина.
        max_height: максимальная высота.
        quality: JPEG-качество (1-100).
    """
    if not image_field:
        return

    try:
        img = Image.open(image_field)
    except Exception:
        return

    img_format = img.format or 'JPEG'

    # Конвертируем в RGB для JPEG
    if img_format.upper() == 'JPEG' and img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
    elif img_format.upper() == 'PNG' and img.mode not in ('RGBA', 'RGB', 'L'):
        img = img.convert('RGBA')

    # Уменьшаем если больше max
    if img.width > max_width or img.height > max_height:
        img.thumbnail((max_width, max_height), Image.LANCZOS)

    # Сохраняем в буфер
    output = BytesIO()
    if img_format.upper() == 'PNG':
        img.save(output, format='PNG', optimize=True)
    else:
        img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)

    # Перезаписываем файл
    image_field.save(image_field.name, ContentFile(output.read()), save=False)


# ─────────────────────────────────────────────
# Модели
# ─────────────────────────────────────────────
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
        Category,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name=_('Категория'),
    )
    name = models.CharField(_('Название'), max_length=150)
    slug = models.SlugField(_('Slug'), max_length=170, unique=True, blank=True)
    short_description = models.CharField(_('Краткое описание'), max_length=255, blank=True)
    description = models.TextField(_('Полное описание'), blank=True)
    price_from = models.DecimalField(_('Цена от, ₽'), max_digits=10, decimal_places=2)
    image = models.ImageField(_('Главное изображение'), upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(_('Создана'), auto_now_add=True)

    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.category.name} → {self.name}'

    def save(self, *args, **kwargs):
        """Автогенерация slug + ресайз главного изображения."""
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        # Уменьшаем главное фото до 800x800
        if self.image and not self.image._committed:
            _resize_image(self.image, max_width=800, max_height=800)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL на услугу."""
        return reverse('services:detail', kwargs={'slug': self.slug})


class ServiceImage(models.Model):
    """
    Дополнительное изображение услуги (галерея).

    Позволяет загружать несколько фото к одной услуге.
    Каждое фото уменьшается до 1600px и получает миниатюру 300px.
    """

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name=_('Услуга'),
    )
    image = models.ImageField(_('Изображение'), upload_to='services/gallery/')
    thumbnail = models.ImageField(
        _('Миниатюра'),
        upload_to='services/gallery/thumbs/',
        blank=True,
        null=True,
        editable=False,
    )
    alt_text = models.CharField(_('Alt-текст'), max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(_('Порядок'), default=0)
    created_at = models.DateTimeField(_('Загружено'), auto_now_add=True)

    class Meta:
        verbose_name = _('Фото услуги')
        verbose_name_plural = _('Фото услуг')
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'Фото #{self.pk} для «{self.service.name}»'

    def save(self, *args, **kwargs):
        """Уменьшаем оригинал до 1600px и создаём миниатюру 300px."""
        # Ресайз основного изображения
        if self.image and not self.image._committed:
            _resize_image(self.image, max_width=1600, max_height=1600)
            self._create_thumbnail()

        super().save(*args, **kwargs)

    def _create_thumbnail(self):
        """Создаёт уменьшенную копию 300x300 для миниатюры."""
        if not self.image:
            return
        try:
            img = Image.open(self.image)
        except Exception:
            return

        img_format = img.format or 'JPEG'
        if img_format.upper() == 'JPEG' and img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        elif img_format.upper() == 'PNG' and img.mode not in ('RGBA', 'RGB', 'L'):
            img = img.convert('RGBA')

        img.thumbnail((300, 300), Image.LANCZOS)

        output = BytesIO()
        if img_format.upper() == 'PNG':
            img.save(output, format='PNG', optimize=True)
            ext = 'png'
        else:
            img.save(output, format='JPEG', quality=85, optimize=True)
            ext = 'jpg'
        output.seek(0)

        name = f'thumb_{self.image.name.split("/")[-1].rsplit(".", 1)[0]}.{ext}'
        self.thumbnail.save(name, ContentFile(output.read()), save=False)

    def get_thumb_url(self):
        """Возвращает URL миниатюры (или оригинала, если нет)."""
        if self.thumbnail:
            return self.thumbnail.url
        return self.image.url if self.image else ''