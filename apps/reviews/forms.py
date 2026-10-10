"""Формы reviews."""

from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """Форма отзыва."""

    class Meta:
        model = Review
        fields = ('name', 'rating', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.Select(
                choices=[(i, f'{i}★') for i in range(1, 6)], attrs={'class': 'form-select'}
            ),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
