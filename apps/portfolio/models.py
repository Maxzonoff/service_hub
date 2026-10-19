"""
Модели приложения portfolio: PortfolioWork, PortfolioImage.
"""
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image

from apps.services.models import Category


def _resize_image(image_field, max_width=1600, max_height=1600, quality=85):
    """Уменьшает изображение до указанных размеров."""
    if not image_field:
        return

    try:
        img = Image.open(image_field)
    except Exception:
        return

    img_format = img.format or 'JPEG'
    if img_format.upper() == 'JPEG' and img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
    elif img_format.upper() == 'PNG' and img.mode not in ('RGBA', 'RGB', 'L'):
        img = img.convert('RGBA')

    if img.width > max_width or img.height > max_height:
        img.thumbnail((max_width, max_height), Image.LANCZOS)

    output = BytesIO()
    if img_format.upper() == 'PNG':
        img.save(output, format='PNG', optimize=True)
    else:
        img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)

    image_field.save(image_field.name, ContentFile(output.read()), save=False)


class PortfolioWork(models.Model):
    """
    Работа в портфолио.

    Содержит главное фото, категорию, описание.
    Дополнительные фото — в PortfolioImage.
    """

    title = models.CharField(_('Название'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='portfolio_works',
        verbose_name=_('Категория'),
    )
    description = models.TextField(_('Описание'), blank=True)
    main_image = models.ImageField(_('Главное фото'), upload_to='portfolio/')
    order = models.PositiveSmallIntegerField(_('Порядок'), default=0)
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(_('Создана'), auto_now_add=True)

    class Meta:
        verbose_name = _('Работа')
        verbose_name_plural = _('Работы')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Авто-slug + ресайз главного фото."""
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.main_image and not self.main_image._committed:
            _resize_image(self.main_image, max_width=1600, max_height=1600)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL на работу."""
        return reverse('portfolio:detail', kwargs={'pk': self.pk})


class PortfolioImage(models.Model):
    """Дополнительное фото в работе."""

    work = models.ForeignKey(
        PortfolioWork,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Работа'),
    )
    image = models.ImageField(_('Изображение'), upload_to='portfolio/gallery/')
    thumbnail = models.ImageField(
        _('Миниатюра'),
        upload_to='portfolio/gallery/thumbs/',
        blank=True,
        null=True,
        editable=False,
    )
    alt_text = models.CharField(_('Alt-текст'), max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(_('Порядок'), default=0)
    created_at = models.DateTimeField(_('Загружено'), auto_now_add=True)

    class Meta:
        verbose_name = _('Фото работы')
        verbose_name_plural = _('Фото работ')
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'Фото #{self.pk} для «{self.work.title}»'

    def save(self, *args, **kwargs):
        """Уменьшаем оригинал и создаём миниатюру."""
        if self.image and not self.image._committed:
            _resize_image(self.image, max_width=1600, max_height=1600)
            self._create_thumbnail()
        super().save(*args, **kwargs)

    def _create_thumbnail(self):
        """Создаёт миниатюру 300×300."""
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
        """URL миниатюры (или оригинала)."""
        if self.thumbnail:
            return self.thumbnail.url
        return self.image.url if self.image else ''