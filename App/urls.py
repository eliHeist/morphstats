from django.urls import path

from App.views import LatestStatDetailView, StatDetailView, StatListView, registerDayView


app_name = "App"

urlpatterns = [
    path('', StatListView.as_view(), name='stat-list'),
    path('stats/<int:pk>/', StatDetailView.as_view(), name='stat-detail'),
    path('stats/latest/', LatestStatDetailView.as_view(), name='latest-stat'),
    path('newday/', registerDayView, name='register-day'),
]