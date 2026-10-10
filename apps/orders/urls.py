"""URL-маршруты orders."""

from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('success/<str:number>/', views.OrderSuccessView.as_view(), name='success'),
    path('<str:number>/', views.OrderDetailView.as_view(), name='detail'),
]
