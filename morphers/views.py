from django.shortcuts import render
from django.views.generic import ListView, DetailView

from morphers.models import Morpher
from stats.models import Day
from stats.views import Counter, getPresent



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

def attendanceStatus(object, days):
    dayz = []
    for day in days:
        present = getPresent(day)
        if object in present:
            dayz.append({'date':day.date.strftime('%A %d, %B %Y'),'status':'Present'})
        else:
            dayz.append({'date':day.date.strftime('%A %d, %B %Y'),'status':'Absent'})
    return dayz


class MorpherDetailView(DetailView):
    model = Morpher
    context_object_name = 'morpher'
    template_name = "morphers/detail.html"

    def get_context_data(self, **kwargs):
        context = super(MorpherDetailView, self).get_context_data(**kwargs)
        days = Day.objects.all().order_by('-date')[:5]
        dayz = attendanceStatus(self.object, days)
        

        context['days'] = dayz
        return context
