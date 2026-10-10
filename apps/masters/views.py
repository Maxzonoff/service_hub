"""Представления masters."""

from django.views.generic import DetailView, ListView

from .models import Master


class MasterListView(ListView):
    """Список мастеров."""

    model = Master
    template_name = 'masters/list.html'
    context_object_name = 'masters'
    queryset = Master.objects.filter(is_active=True).prefetch_related('specialization')


class MasterDetailView(DetailView):
    """Страница мастера."""

    model = Master
    template_name = 'masters/detail.html'
    context_object_name = 'master'

    def get_context_data(self, **kwargs):
        """Добавляет работы."""
        ctx = super().get_context_data(**kwargs)
        ctx['works'] = self.object.works.all()
        return ctx
