from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, CreateView

from facilitators.models import Facilitator, PrayerRequest

# Create your views here.
class FacilitatorListView(ListView):
    model = Facilitator
    context_object_name = 'facilitators'
    template_name = "facilitators/list.html"


class PrayerRequestListView(ListView):
    model = PrayerRequest
    template_name = "facilitators/prayers/list.html"
    context_object_name = 'requests'


class PrayerRequestCreateView(CreateView):
    model = PrayerRequest
    fields = ('facilitator','prayer_request')
    template_name = "facilitators/prayers/create.html"

    def get_success_url(self):
        return reverse('facilitators:prayer-list')


def makeTestimony(request, pk):
    request = PrayerRequest.objects.filter(id=pk).update(is_answered=True)
    return redirect('facilitators:prayer-list')
