from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import apiOverview, facilitatorChecklistView, facilitatorsApiView, serviceApiView, stats
from api import views

app_name = "api"

# Router for ViewSet-based mobile API routes
router = DefaultRouter()
router.register(r'v1/stats', views.StatViewSet, basename='v1-stats')
router.register(r'v1/services', views.ServiceViewSet, basename='v1-services')
router.register(r'v1/facilitators', views.FacilitatorViewSet, basename='v1-facilitators')
router.register(r'v1/tags', views.TagViewSet, basename='v1-tags')
router.register(r'v1/events', views.EventViewSet, basename='v1-events')

urlpatterns = [
    # JWT auth endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # v1 ViewSet routes (mobile API)
    path('', include(router.urls)),

    # Legacy routes (web frontend — do not remove)
    path('overview/', apiOverview, name="overview"),
    path('stats/', stats, name="stats"),
    path('stats/<int:pk>/', stats, name="stats-detail"),
    path('stats/<int:stat_pk>/services', serviceApiView, name="stat-services"),
    path('services/', views.ServiceAPIView.as_view(), name="services"),
    path('stat/<int:stat_pk>/servicelists/', facilitatorChecklistView, name="get-service-lists"),
    path('facilitator-checklist/', facilitatorChecklistView, name="update-facilitators"),
    path('facilitators/', facilitatorsApiView, name="facilitators"),
]
