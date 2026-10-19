"""
Формы приложения services.
"""
from django import forms
from django.utils.text import slugify
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Service


class MultipleFileInput(forms.ClearableFileInput):
    """Виджет для загрузки нескольких файлов сразу."""

    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """
    Поле для загрузки нескольких файлов.

    Работает через MultipleFileInput — Django сам примет список файлов.
    """

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


class ServiceForm(forms.ModelForm):
    """Форма услуги для админов (с поддержкой загрузки галереи)."""

    slug = forms.CharField(
        required=False,
        label='Slug (URL)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Оставьте пустым — сгенерируется автоматически',
        }),
    )

    # Поле галереи — используем собственный MultipleFileField
    gallery_images = MultipleFileField(
        required=False,
        label='Галерея (можно несколько фото)',
        help_text='Выберите сразу несколько фото (Ctrl/Cmd + клик). Каждое уменьшится до 1600px.',
    )

    class Meta:
        model = Service
        fields = (
            'category',
            'name',
            'slug',
            'short_description',
            'description',
            'price_from',
            'image',
            'is_active',
        )
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Замена смесителя',
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кратко, до 255 символов',
            }),
            'description': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'},
                config_name='default',
            ),
            'price_from': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'category': 'Категория',
            'name': 'Название',
            'slug': 'Slug (URL)',
            'short_description': 'Краткое описание',
            'description': 'Полное описание',
            'price_from': 'Цена от, ₽',
            'image': 'Главное изображение',
            'is_active': 'Активна',
        }

    def clean_slug(self):
        """Генерирует slug из названия, если пусто; транслитерирует русский."""
        slug = (self.cleaned_data.get('slug') or '').strip()
        name = (self.cleaned_data.get('name') or '').strip()

        if not slug and name:
            slug = self._make_slug(name)
        if slug and not slug.isascii():
            slug = self._make_slug(slug)

        slug = slugify(slug, allow_unicode=False)

        qs = Service.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                'Услуга с таким slug уже существует. Измените slug или название.'
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