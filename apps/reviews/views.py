"""Представления reviews."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import ListView, View

from .forms import ReviewForm
from .models import Review


class ReviewListView(ListView):
    """Список опубликованных отзывов."""

    model = Review
    template_name = 'reviews/list.html'
    context_object_name = 'reviews'
    paginate_by = 12
    queryset = Review.objects.filter(is_published=True)


class ReviewCreateView(View):
    """Форма добавления отзыва."""

    def get(self, request):
        """Показывает форму."""
        return render(request, 'reviews/form.html', {'form': ReviewForm()})

    def post(self, request):
        """Сохраняет отзыв (уходит на модерацию)."""
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.client = request.user
            review.save()
            messages.success(request, 'Спасибо за отзыв! Он появится после модерации.')
            return redirect('reviews:list')
        return render(request, 'reviews/form.html', {'form': form})
