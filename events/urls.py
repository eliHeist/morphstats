from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('CU/', views.EventCreateUpdateView.as_view(), name='create'),
    path('CU/<int:pk>/', views.EventCreateUpdateView.as_view(), name='update'),
]