from django.urls import path

from morphers.views import morpherListView


app_name = 'morphers'

urlpatterns = [
    path('', morpherListView, name='list')
]