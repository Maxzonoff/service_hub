"""URL-маршруты services."""

from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='detail'),
]
