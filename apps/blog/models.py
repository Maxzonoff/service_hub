"""Модели blog: Post, Tag."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field


class Tag(models.Model):
    """Тег статьи."""

    name = models.CharField(_('Название'), max_length=50, unique=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)

    class Meta:
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Авто-slug."""
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Статья блога."""

    title = models.CharField(_('Заголовок'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=220, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name=_('Автор'),
    )
    cover = models.ImageField(_('Обложка'), upload_to='blog/', blank=True, null=True)
    excerpt = models.CharField(_('Краткое описание'), max_length=300, blank=True)
    content = CKEditor5Field(_('Содержимое'), config_name='default')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name=_('Теги'))
    is_published = models.BooleanField(_('Опубликована'), default=False)
    published_at = models.DateTimeField(_('Дата публикации'), default=timezone.now)
    views_count = models.PositiveIntegerField(_('Просмотров'), default=0)
    meta_title = models.CharField(_('Meta title'), max_length=200, blank=True)
    meta_description = models.CharField(_('Meta description'), max_length=300, blank=True)
    created_at = models.DateTimeField(_('Создана'), auto_now_add=True)

    class Meta:
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Авто-slug."""
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL на статью."""
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def increment_views(self):
        """Увеличивает счётчик просмотров."""
        Post.objects.filter(pk=self.pk).update(views_count=models.F('views_count') + 1)
