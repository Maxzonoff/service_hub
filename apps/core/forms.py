"""Формы core."""

from django import forms

from .models import CallbackRequest


class CallbackForm(forms.ModelForm):
    """Форма обратного звонка."""

    class Meta:
        model = CallbackRequest
        fields = ('name', 'phone', 'comment')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '+7 999 123-45-67'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Комментарий (необязательно)',
                }
            ),
        }
