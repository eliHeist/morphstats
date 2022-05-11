import json
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from stats.models import Day
from stats.views import getPresent

# Create your views here.

def landingView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    template_name = "main/dashboard.html"

    days = Day.objects.all().order_by('date')[:5]
    listarray = []

    for day in days:
        count = getPresent(day)
        inv = {'date':day.date.strftime("%d %b"), 'count':len(count)}
        # inv = {'date':day.date.strftime("%a %d %b %Y"), 'count':len(count)}
        listarray.append(inv)

    context = {
        'data': json.dumps(listarray),
    }
    return render(request, template_name, context)
