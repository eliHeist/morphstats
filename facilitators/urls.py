from django.urls import path

from facilitators.views import FacilitatorListView

app_name = 'facilitators'

urlpatterns = [
    path('', FacilitatorListView.as_view(), name='list')
]