"""Представления accounts."""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import User


class RegisterView(CreateView):
    """Регистрация нового пользователя."""

    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:profile')

    def dispatch(self, request, *args, **kwargs):
        """Перенаправляет залогиненных на профиль."""
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Сохраняет, логинит, показывает уведомление."""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Добро пожаловать, {self.object.first_name}!')
        return response


class LoginView(DjangoLoginView):
    """Вход в личный кабинет."""

    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """URL после входа."""
        return reverse_lazy('accounts:profile')

    def form_valid(self, form):
        """Приветствие после входа."""
        messages.success(self.request, f'С возвращением, {form.get_user().get_short_name()}!')
        return super().form_valid(form)


class LogoutView(View):
    """Выход из личного кабинета."""

    def post(self, request, *args, **kwargs):
        """Разлогинивает и редиректит на главную."""
        logout(request)
        messages.info(request, 'Вы вышли из системы.')
        return redirect('core:home')

    def get(self, request, *args, **kwargs):
        """На GET тоже разлогинивает."""
        return self.post(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, View):
    """Личный кабинет пользователя."""

    def get(self, request, *args, **kwargs):
        """Показывает профиль и заказы."""
        orders = request.user.orders.all()[:10] if hasattr(request.user, 'orders') else []
        return render(
            request, 'accounts/profile.html', {'user_obj': request.user, 'orders': orders}
        )


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля."""

    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        """Возвращает текущего пользователя."""
        return self.request.user

    def form_valid(self, form):
        """Сохраняет и уведомляет."""
        messages.success(self.request, 'Профиль обновлён.')
        return super().form_valid(form)
