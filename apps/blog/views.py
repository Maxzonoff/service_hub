"""Представления blog."""

from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    """Список статей."""

    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9
    queryset = (
        Post.objects.filter(is_published=True).select_related('author').prefetch_related('tags')
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
            Post.objects.filter(is_published=True, tags__in=self.object.tags.all())
            .exclude(pk=self.object.pk)
            .distinct()[:3]
        )
        return ctx
