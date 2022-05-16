from django.urls import path

from facilitators.views import FacilitatorListView, PrayerRequestCreateView, PrayerRequestListView, makeTestimony

app_name = 'facilitators'

urlpatterns = [
    path('', FacilitatorListView.as_view(), name='list'),
    path('prayerrequests/', PrayerRequestListView.as_view(), name='prayer-list'),
    path('prayerrequests/create/', PrayerRequestCreateView.as_view(), name='prayer-create'),
    path('prayerrequests/<int:pk>/maketestimony/', makeTestimony, name='prayer-answered'),
]