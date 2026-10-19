"""
Представления приложения blog.

Публичные:
- список статей
- детальная статья

Для админов (is_staff=True):
- создание статьи
- редактирование статьи
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    """Список опубликованных статей."""

    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        """Только опубликованные, с оптимизацией запросов."""
        return (
            Post.objects
            .filter(is_published=True)
            .select_related('author')
            .prefetch_related('tags')
        )


class PostDetailView(DetailView):
    """Страница статьи."""

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Находит по slug и увеличивает просмотры."""
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        """Добавляет похожие статьи."""
        ctx = super().get_context_data(**kwargs)
        ctx['related'] = (
            Post.objects
            .filter(is_published=True, tags__in=self.object.tags.all())
            .exclude(pk=self.object.pk)
            .distinct()[:3]
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
        """Реакция, если не админ."""
        messages.error(self.request, 'У вас нет прав для этого действия.')
        return redirect('blog:list')


class PostCreateView(StaffRequiredMixin, CreateView):
    """Создание новой статьи (только для админов)."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        """Сохраняет статью, привязывает автора."""
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Статья «{self.object.title}» успешно создана.')
        return response

    def get_context_data(self, **kwargs):
        """Флаги для шаблона."""
        ctx = super().get_context_data(**kwargs)
        ctx['is_create'] = True
        ctx['form_title'] = 'Новая статья'
        ctx['submit_label'] = 'Создать статью'
        return ctx


class PostUpdateView(StaffRequiredMixin, UpdateView):
    """Редактирование статьи (только для админов)."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        """После сохранения — на страницу статьи."""
        return reverse_lazy('blog:detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        """Сохраняет и уведомляет."""
        response = super().form_valid(form)
        messages.success(self.request, f'Статья «{self.object.title}» обновлена.')
        return response

    def get_context_data(self, **kwargs):
        """Флаги для шаблона."""
        ctx = super().get_context_data(**kwargs)
        ctx['is_create'] = False
        ctx['form_title'] = f'Редактировать: {self.object.title}'
        ctx['submit_label'] = 'Сохранить изменения'
        return ctx