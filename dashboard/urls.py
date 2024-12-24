from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Define your URL patterns here
    path('', views.StatisticsDashboardView.as_view(), name='index'),
]