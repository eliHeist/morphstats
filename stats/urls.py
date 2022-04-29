from django.urls import path

from stats.views import dayDetailView, dayListView, serviceDetailView, statsView

app_name = 'stats'

urlpatterns = [
    path('', dayListView, name='days-list'),
    path('day/<int:pk>/', dayDetailView, name='day-detail'),
    path('services/<int:pk>/', serviceDetailView, name='service-stats'),
    path('stats/', statsView, name='stats'),
]