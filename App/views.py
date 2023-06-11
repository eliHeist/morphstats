from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView

from Stat.models import Service, Stat

# Create your views here.
class StatListView(ListView):
    model = Stat
    template_name = 'App/stats-list.html'
    context_object_name = 'stats'

    def get_queryset(self):
        return Stat.objects.all().order_by('-date')


class StatDetailView(DetailView):
    model = Stat
    template_name = 'App/stats-detail.html'
    context_object_name = 'stat'


class LatestStatDetailView(TemplateView):
    template_name = 'App/stats-detail.html'
    context_object_name = 'stat'

    def get_queryset(self):
        return Stat.objects.all().order_by('-date').first()

    def get_context_data(self, **kwargs):
        context = super(LatestStatDetailView, self).get_context_data(**kwargs)
        context['stat'] = self.get_queryset()
        context['link_name'] = 'latest-stat'
        return context


def registerDayView(request):
    if request.method == 'POST':
        data = request.POST
        date = data.get('date')
        title = data.get('title')
        first_service = data.get('first_service')
        second_service = data.get('second_service')
        third_service = data.get('third_service')

        Stat(date=date, title=title).save()
        stat = Stat.objects.last()
        
        if first_service:
            Service(stat=stat, name='1st').save()
        if second_service:
            Service(stat=stat, name='2nd').save()
        if third_service:
            Service(stat=stat, name='3rd').save()
        
        return redirect('App:stat-list')
            
            
    context = {}
    template_name = 'App/register-day.html'
    return render(request, template_name, context)

def page_not_found(request, exception):
    return render(request, '404.html', status=404)
