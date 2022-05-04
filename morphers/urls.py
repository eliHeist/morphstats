from django.urls import path

from morphers.views import MorpherDetailView, morpherListView


app_name = 'morphers'

urlpatterns = [
    path('', morpherListView, name='list'),
    path('<int:pk>/', MorpherDetailView.as_view(), name='detail'),
]