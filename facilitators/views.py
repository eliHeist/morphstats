from django.shortcuts import render
from django.views.generic import ListView

from facilitators.models import Facilitator

# Create your views here.
class FacilitatorListView(ListView):
    model = Facilitator
    context_object_name = 'facilitators'
    template_name = "facilitators/list.html"
