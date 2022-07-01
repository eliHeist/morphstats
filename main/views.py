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

    day_count = Day.objects.count()
    # for last 2
    min_index = day_count-5 if day_count>5 else 0
    days = Day.objects.all()[min_index:]
    # print(day_count)
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
