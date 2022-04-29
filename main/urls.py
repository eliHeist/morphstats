from django.urls import path

from main.views import LandingView

app_name = 'main'

urlpatterns = [
    path('', LandingView.as_view(),name='dashboard'),
]