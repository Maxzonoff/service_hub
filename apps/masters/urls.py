"""URL-маршруты masters."""

from django.urls import path

from . import views

app_name = 'masters'

urlpatterns = [
    path('', views.MasterListView.as_view(), name='list'),
    path('<int:pk>/', views.MasterDetailView.as_view(), name='detail'),
]
