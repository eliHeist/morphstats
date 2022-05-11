from django.urls import path

from main.views import landingView

app_name = 'main'

urlpatterns = [
    path('', landingView, name='dashboard'),
]