from django.shortcuts import render
from django.views.generic import ListView

from morphers.models import Morpher
from stats.views import Counter



# Create your views here.
class MorpherListView(ListView):
    model = Morpher
    context_object_name = 'morphers'
    template_name = "morphers/list.html"

def morpherListView(request):
    morphers = Morpher.objects.all()
    counter = Counter()
    template_name = "morphers/list.html"

    context = {
        'morphers':morphers,
        'counter':counter,
    }
    return render(request, template_name, context)