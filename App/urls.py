from django.urls import path

from App.views import StatDetailView, StatListView, registerDayView


app_name = "App"

urlpatterns = [
    path('', StatListView.as_view(), name='stat-list'),
    path('stats/<int:pk>/', StatDetailView.as_view(), name='stat-detail'),
    path('newday/', registerDayView, name='register-day'),
]