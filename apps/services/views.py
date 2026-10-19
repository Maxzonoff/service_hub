"""Представления приложения services."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ServiceForm
from .models import Category, Service, ServiceImage


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
    """Список всех активных услуг."""

    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        """Все активные услуги."""
        return (
            Service.objects
            .filter(is_active=True)
            .select_related('category')
            .order_by('category__order', 'name')
        )

    def get_context_data(self, **kwargs):
        """Категории для блока навигации."""
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(is_active=True)[:8]
        return ctx


class ServiceDetailView(DetailView):
    """Детальная страница услуги."""

    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Добавляет похожие и галерею."""
        ctx = super().get_context_data(**kwargs)
        ctx['related'] = (
            Service.objects
            .filter(category=self.object.category, is_active=True)
            .exclude(pk=self.object.pk)[:4]
        )
        ctx['gallery'] = self.object.gallery.all()
        return ctx


# ─────────────────────────────────────────────
# Админ-часть
# ─────────────────────────────────────────────
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Доступ только is_staff."""

    def test_func(self):
        """Только админ."""
        return self.request.user.is_staff

    def handle_no_permission(self):
        """Реакция, если не админ."""
        messages.error(self.request, 'У вас нет прав для этого действия.')
        return redirect('services:list')


class ServiceCreateView(StaffRequiredMixin, CreateView):
    """Создание новой услуги на сайте (только для админов)."""

    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:list')

    def form_valid(self, form):
        """Сохраняет услугу и загружает галерею."""
        response = super().form_valid(form)
        self._save_gallery()
        messages.success(self.request, f'Услуга «{self.object.name}» успешно добавлена.')
        return response

    def _save_gallery(self):
        """Сохраняет все загруженные фото в ServiceImage."""
        files = self.request.FILES.getlist('gallery_images')
        for idx, f in enumerate(files):
            ServiceImage.objects.create(service=self.object, image=f, order=idx)

    def get_context_data(self, **kwargs):
        """Передаёт флаги для шаблона."""
        ctx = super().get_context_data(**kwargs)
        ctx['is_create'] = True
        ctx['form_title'] = 'Добавить услугу'
        ctx['submit_label'] = 'Создать услугу'
        return ctx


class ServiceUpdateView(StaffRequiredMixin, UpdateView):
    """Редактирование услуги (только для админов)."""

    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        """После сохранения — на страницу услуги."""
        return reverse_lazy('services:detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        """Сохраняет и добавляет новые фото в галерею."""
        response = super().form_valid(form)
        self._save_gallery()
        messages.success(self.request, f'Услуга «{self.object.name}» обновлена.')
        return response

    def _save_gallery(self):
        """Добавляет новые фото к существующей галерее."""
        files = self.request.FILES.getlist('gallery_images')
        start_order = self.object.gallery.count()
        for idx, f in enumerate(files):
            ServiceImage.objects.create(service=self.object, image=f, order=start_order + idx)

    def get_context_data(self, **kwargs):
        """Флаги для шаблона + галерея."""
        ctx = super().get_context_data(**kwargs)
        ctx['is_create'] = False
        ctx['form_title'] = f'Редактировать: {self.object.name}'
        ctx['submit_label'] = 'Сохранить изменения'
        ctx['gallery'] = self.object.gallery.all()
        return ctx