"""URL-маршруты приложения blog."""
from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('add/', views.PostCreateView.as_view(), name='add'),
    path('<slug:slug>/edit/', views.PostUpdateView.as_view(), name='edit'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
]