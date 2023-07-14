from django.urls import path

from App.views import AccessDeniedView, FacilitatorChecklistView, FacilitatorCreateView, FacilitatorListView, LatestStatDetailView, MoreMenuView, RegisterDayView, StatDetailView, StatListView


app_name = "App"

urlpatterns = [
    path('', StatListView.as_view(), name='stat-list'),
    path('stats/<int:pk>/', StatDetailView.as_view(), name='stat-detail'),
    path('stats/latest/', LatestStatDetailView.as_view(), name='latest-stat'),
    path('newday/', RegisterDayView.as_view(), name='register-day'),
    path('facilitators/', FacilitatorListView.as_view(), name="facilitator-list"),
    path('facilitators/create/', FacilitatorCreateView.as_view(), name="facilitator-create"),
    path('facilitators/checklist/', FacilitatorChecklistView.as_view(), name='facilitator-checklist'),
    path('moreinfo/', MoreMenuView.as_view(), name='info'),

    path('access-denied/', AccessDeniedView.as_view(), name='access-denied')
]