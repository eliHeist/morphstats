from django.urls import path

from api.views import apiOverview, facilitatorChecklistView, facilitatorsApiView, serviceApiView, stats

app_name = "api"

urlpatterns = [
    path('', apiOverview, name="overview"),
    path('stats/', stats, name="stats"),
    path('stats/<int:pk>/', stats, name="stats-detail"),
    path('stats/<int:stat_pk>/services', serviceApiView, name="stat-services"),
    path('services/', serviceApiView, name="services"),
    path('stat/<int:stat_pk>/servicelists/', facilitatorChecklistView, name="get-service-lists"),
    path('facilitator-checklist/', facilitatorChecklistView, name="update-facilitators"),
    path('facilitators/', facilitatorsApiView, name="facilitators"),
]