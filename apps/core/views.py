"""Представления core: главная, о нас, контакты."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from apps.services.models import Category, Service
from apps.reviews.models import Review

from .forms import CallbackForm
from .models import Advantage, FAQ, SiteSettings


class HomeView(View):
    """Главная страница."""

    def get(self, request):
        """Рендерит главную с блоками услуг, преимуществ, отзывов."""
        context = {
            'categories': Category.objects.filter(is_active=True)[:8],
            'popular_services': Service.objects.filter(is_active=True)[:6],
            'advantages': Advantage.objects.filter(is_active=True),
            'reviews': Review.objects.filter(is_published=True)[:6],
            'faqs': FAQ.objects.filter(is_active=True),
            'callback_form': CallbackForm(),
        }
        return render(request, 'core/home.html', context)


class AboutView(TemplateView):
    """О нас."""

    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        """Добавляет преимущества."""
        ctx = super().get_context_data(**kwargs)
        ctx['advantages'] = Advantage.objects.filter(is_active=True)
        return ctx


class ContactsView(View):
    """Контакты с формой обратного звонка."""

    def get(self, request):
        """Рендерит страницу контактов."""
        return render(
            request,
            'core/contacts.html',
            {
                'site_settings': SiteSettings.load(),
                'callback_form': CallbackForm(),
            },
        )

    def post(self, request):
        """Обрабатывает заявку на обратный звонок."""
        form = CallbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка принята. Мы перезвоним в течение 15 минут.')
            return redirect('core:contacts')
        return render(
            request,
            'core/contacts.html',
            {
                'site_settings': SiteSettings.load(),
                'callback_form': form,
            },
        )