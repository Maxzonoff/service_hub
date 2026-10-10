"""Формы accounts: регистрация, вход, профиль."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
    )
    first_name = forms.CharField(
        label='Имя', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 999 123-45-67'}),
    )
    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')

    def clean_email(self):
        """Проверяет уникальность email."""
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def clean_phone(self):
        """Проверяет уникальность телефона."""
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким телефоном уже зарегистрирован.')
        return phone

    def save(self, commit=True):
        """Сохраняет пользователя."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Форма входа по email и паролю."""

    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
    )
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ProfileForm(forms.ModelForm):
    """Форма редактирования профиля."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'address', 'avatar')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        """Проверяет уникальность телефона."""
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Этот телефон уже используется.')
        return phone
