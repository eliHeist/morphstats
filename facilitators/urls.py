from django.urls import path
from facilitators import views

app_name = "facilitators"

urlpatterns = [
    path('attendance/', views.AttendanceView.as_view(), name='attendance'),
]