"""Представления services."""

from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Category, Service


class CategoryListView(ListView):
    """Список всех категорий."""

    model = Category
    template_name = 'services/category_list.html'
    context_object_name = 'categories'
    queryset = Category.objects.filter(is_active=True)


class CategoryDetailView(DetailView):
    """Услуги одной категории."""

    model = Category
    template_name = 'services/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Добавляет список услуг."""
        ctx = super().get_context_data(**kwargs)
        ctx['services'] = self.object.services.filter(is_active=True)
        return ctx


class ServiceListView(ListView):
    """Список всех услуг."""

    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        """Фильтрует по категории, если передан slug."""
        qs = Service.objects.filter(is_active=True).select_related('category')
        cat = self.request.GET.get('category')
        if cat:
            qs = qs.filter(category__slug=cat)
        return qs


class ServiceDetailView(DetailView):
    """Детальная страница услуги."""

    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Добавляет похожие услуги."""
        ctx = super().get_context_data(**kwargs)
        ctx['related'] = Service.objects.filter(
            category=self.object.category, is_active=True
        ).exclude(pk=self.object.pk)[:4]
        return ctx
