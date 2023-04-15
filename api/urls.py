from django.urls import path

from api.views import apiOverview, serviceApiView, stats

app_name = "api"

urlpatterns = [
    path('', apiOverview, name="overview"),
    path('stats/', stats, name="stats"),
    path('stats/<int:pk>/', stats, name="stats-detail"),
    path('stats/<int:stat_pk>/services', serviceApiView, name="stat-services"),
]