"""Формы orders."""

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """Форма оформления заказа."""

    class Meta:
        model = Order
        fields = (
            'name',
            'phone',
            'email',
            'service',
            'address',
            'preferred_date',
            'comment',
            'promo_code',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '+7 999 123-45-67'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'you@example.com'}
            ),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Город, улица, дом, квартира'}
            ),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Что нужно сделать?'}
            ),
            'promo_code': forms.Select(attrs={'class': 'form-select'}),
        }
