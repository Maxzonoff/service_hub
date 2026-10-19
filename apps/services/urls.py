"""URL-маршруты приложения services."""
from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    # Админ-маршруты (должны идти ДО slug, чтобы не конфликтовать)
    path('add/', views.ServiceCreateView.as_view(), name='add'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('<slug:slug>/edit/', views.ServiceUpdateView.as_view(), name='edit'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='detail'),
]