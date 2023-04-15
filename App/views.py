from django.shortcuts import render
from django.views.generic import ListView, DetailView

from Stat.models import Stat

# Create your views here.
class StatListView(ListView):
    model = Stat
    template_name = 'App/stats-list.html'
    context_object_name = 'stats'


class StatDetailView(DetailView):
    model = Stat
    template_name = 'App/stats-detail.html'
    context_object_name = 'stat'