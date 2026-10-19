"""Формы приложения portfolio (для будущего управления с сайта)."""
from django import forms

from .models import PortfolioWork


class MultipleFileInput(forms.ClearableFileInput):
    """Виджет для нескольких файлов."""

    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Поле для нескольких файлов."""

    def __init__(self, *args, **kwargs):
        """Задаём виджет."""
        kwargs.setdefault('widget', MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """Список очищенных файлов."""
        single = super().clean
        if isinstance(data, (list, tuple)):
            return [single(d, initial) for d in data]
        return [single(data, initial)] if data else []


class PortfolioWorkForm(forms.ModelForm):
    """Форма работы для админов."""

    gallery_images = MultipleFileField(
        required=False,
        label='Дополнительные фото',
        help_text='Выберите сразу несколько.',
    )

    class Meta:
        model = PortfolioWork
        fields = ('title', 'slug', 'category', 'description', 'main_image', 'order', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Название',
            'slug': 'Slug',
            'category': 'Категория',
            'description': 'Описание',
            'main_image': 'Главное фото',
            'order': 'Порядок',
            'is_active': 'Активна',
        }

    def clean_slug(self):
        """Автогенерация slug из title, если пусто."""
        from django.utils.text import slugify
        slug = (self.cleaned_data.get('slug') or '').strip()
        title = (self.cleaned_data.get('title') or '').strip()
        if not slug and title:
            slug = slugify(title, allow_unicode=False)
        return slug