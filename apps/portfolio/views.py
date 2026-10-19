"""
Представления портфолио.

Публичные:
- список работ с фильтром по категории
- детальная работа

Для админов (is_staff=True):
- создание работы
- редактирование работы
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.services.models import Category

from .forms import PortfolioWorkForm
from .models import PortfolioImage, PortfolioWork


class WorkListView(ListView):
    """Список всех работ с фильтром по категории."""

    model = PortfolioWork
    template_name = 'portfolio/list.html'
    context_object_name = 'works'
    paginate_by = 12

    def get_queryset(self):
        """Активные работы + фильтр по категории из GET."""
        qs = (
            PortfolioWork.objects
            .filter(is_active=True)
            .select_related('category')
            .prefetch_related('images')
        )
        cat = self.request.GET.get('category')
        if cat:
            qs = qs.filter(category__slug=cat)
        return qs

    def get_context_data(self, **kwargs):
        """Категории для фильтра."""
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(is_active=True)
        ctx['current_category'] = self.request.GET.get('category', '')
        return ctx


class WorkDetailView(DetailView):
    """Детальная страница работы."""

    model = PortfolioWork
    template_name = 'portfolio/detail.html'
    context_object_name = 'work'

    def get_context_data(self, **kwargs):
        """Добавляет галерею и похожие работы."""
        ctx = super().get_context_data(**kwargs)
        ctx['gallery'] = self.object.images.all()
        ctx['related'] = (
            PortfolioWork.objects
            .filter(is_active=True, category=self.object.category)
            .exclude(pk=self.object.pk)[:4]
        )
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
        """Реакция."""
        messages.error(self.request, 'У вас нет прав для этого действия.')
        return redirect('portfolio:list')


class WorkCreateView(StaffRequiredMixin, CreateView):
    """Создание работы."""

    model = PortfolioWork
    form_class = PortfolioWorkForm
    template_name = 'portfolio/work_form.html'
    success_url = reverse_lazy('portfolio:list')

    def form_valid(self, form):
        """Сохраняет работу + галерею."""
        response = super().form_valid(form)
        self._save_gallery()
        messages.success(self.request, f'Работа «{self.object.title}» добавлена.')
        return response

    def _save_gallery(self):
        """Сохраняет все загруженные фото."""
        files = self.request.FILES.getlist('gallery_images')
        for idx, f in enumerate(files):
            PortfolioImage.objects.create(work=self.object, image=f, order=idx)

    def get_context_data(self, **kwargs):
        """Флаги для шаблона."""
        ctx = super().get_context_data(**kwargs)
        ctx['is_create'] = True
        ctx['form_title'] = 'Добавить работу'
        ctx['submit_label'] = 'Создать работу'
        return ctx


class WorkUpdateView(StaffRequiredMixin, UpdateView):
    """Редактирование работы."""

    model = PortfolioWork
    form_class = PortfolioWorkForm
    template_name = 'portfolio/work_form.html'

    def get_success_url(self):
        """После сохранения — на страницу работы."""
        return reverse_lazy('portfolio:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """Сохраняет + добавляет новые фото."""
        response = super().form_valid(form)
        self._save_gallery()
        messages.success(self.request, f'Работа «{self.object.title}» обновлена.')
        return response

    def _save_gallery(self):
        """Добавляет новые фото к галерее."""
        files = self.request.FILES.getlist('gallery_images')
        start = self.object.images.count()
        for idx, f in enumerate(files):
            PortfolioImage.objects.create(work=self.object, image=f, order=start + idx)

    def get_context_data(self, **kwargs):
        """Флаги + галерея."""
        ctx = super().get_context_data(**kwargs)
        ctx['is_create'] = False
        ctx['form_title'] = f'Редактировать: {self.object.title}'
        ctx['submit_label'] = 'Сохранить изменения'
        ctx['gallery'] = self.object.images.all()
        return ctx