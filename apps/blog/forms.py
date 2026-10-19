"""
Формы приложения blog.

Используются для создания и редактирования статей
непосредственно на сайте (только для администраторов).
"""
from django import forms
from django.utils.text import slugify
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Post, Tag


class MultipleFileInput(forms.ClearableFileInput):
    """Виджет для загрузки нескольких файлов сразу."""

    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Поле для загрузки нескольких файлов."""

    def __init__(self, *args, **kwargs):
        """Задаём виджет MultipleFileInput."""
        kwargs.setdefault('widget', MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """Возвращает список очищенных файлов."""
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_clean(d, initial) for d in data]
        return [single_clean(data, initial)] if data else []


class PostForm(forms.ModelForm):
    """Форма статьи для админов (с CKEditor 5)."""

    slug = forms.CharField(
        required=False,
        label='Slug (URL)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Оставьте пустым — сгенерируется автоматически',
        }),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label='Теги',
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
    )

    class Meta:
        model = Post
        fields = (
            'title',
            'slug',
            'cover',
            'excerpt',
            'content',
            'tags',
            'is_published',
            'meta_title',
            'meta_description',
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Как выбрать сантехника',
            }),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'excerpt': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание, до 300 символов',
            }),
            'content': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'},
                config_name='default',
            ),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Meta title (для SEO)',
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Meta description (для SEO)',
            }),
        }
        labels = {
            'title': 'Заголовок',
            'slug': 'Slug (URL)',
            'cover': 'Обложка',
            'excerpt': 'Краткое описание',
            'content': 'Содержимое статьи',
            'tags': 'Теги',
            'is_published': 'Опубликовать',
            'meta_title': 'Meta title',
            'meta_description': 'Meta description',
        }

    def clean_slug(self):
        """Генерирует slug из заголовка, если пусто; транслитерирует."""
        slug = (self.cleaned_data.get('slug') or '').strip()
        title = (self.cleaned_data.get('title') or '').strip()

        if not slug and title:
            slug = self._make_slug(title)
        if slug and not slug.isascii():
            slug = self._make_slug(slug)

        slug = slugify(slug, allow_unicode=False)

        qs = Post.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                'Статья с таким slug уже существует. Измените slug или заголовок.'
            )
        return slug

    @staticmethod
    def _make_slug(text):
        """Транслитерация RU → LATIN."""
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            ' ': '-', '_': '-',
        }
        result = []
        for char in text.lower():
            if char in translit_map:
                result.append(translit_map[char])
            elif char.isalnum() and char.isascii():
                result.append(char)
            elif char in '-_':
                result.append('-')
        slug = ''.join(result)
        while '--' in slug:
            slug = slug.replace('--', '-')
        return slug.strip('-')