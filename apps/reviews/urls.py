"""URL-маршруты reviews."""

from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='list'),
    path('add/', views.ReviewCreateView.as_view(), name='add'),
]
