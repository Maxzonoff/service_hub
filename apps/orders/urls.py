"""URL-маршруты приложения orders."""
from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('success/<str:number>/', views.OrderSuccessView.as_view(), name='success'),
    # API-эндпоинты чата (по pk)
    path('<int:pk>/messages/', views.order_messages, name='messages'),
    path('<int:pk>/message/', views.order_message_create, name='message_create'),
    # Просмотр заказа по номеру
    path('<str:number>/', views.OrderDetailView.as_view(), name='detail'),
]