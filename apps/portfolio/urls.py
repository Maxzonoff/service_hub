"""URL-маршруты портфолио."""
from django.urls import path

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.WorkListView.as_view(), name='list'),
    path('add/', views.WorkCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.WorkUpdateView.as_view(), name='edit'),
    path('<int:pk>/', views.WorkDetailView.as_view(), name='detail'),
]