from datetime import date

from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from App.mixins import RedirectNonStaffMixin
from django.utils import timezone

from Stat.models import Service, Stat
from facilitators.forms import FacilitatorForm
from facilitators.models import Facilitator

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

class RegisterDayView(RedirectNonStaffMixin, View):
    def post(self, request):
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
    
    def get(self, request):
        context = {}
        template_name = 'App/register-day.html'
        return render(request, template_name, context)

class FacilitatorChecklistView(RedirectNonStaffMixin, View):
    def get(self, request):
        context = {
            'stat': Stat.objects.all().order_by('-date').first(),
            'link_name': 'facilitators-link',
            'facilitators': 'facilitators-link',
        }
        template_name = 'App/facilitators/facilitator-checklist.html'
        return render(request, template_name, context)
    
class FacilitatorCreateView(RedirectNonStaffMixin, CreateView):
    model = Facilitator
    form_class = FacilitatorForm
    template_name = "App/facilitators/create.html"
    success_url = reverse_lazy('App:facilitator-list')

    def get_context_data(self, **kwargs):
        context = super(FacilitatorCreateView, self).get_context_data(**kwargs)
        context['link_name'] = 'facilitators-link'
        return context
    
class FacilitatorUpdateView(RedirectNonStaffMixin, UpdateView):
    model = Facilitator
    form_class = FacilitatorForm
    template_name = "App/facilitators/edit.html"
    success_url = reverse_lazy('App:facilitator-list')

    def get_context_data(self, **kwargs):
        context = super(FacilitatorUpdateView, self).get_context_data(**kwargs)
        context['link_name'] = 'facilitators-link'
        return context
     
class FacilitatorListView(ListView):
    model = Facilitator
    context_object_name = 'facilitators'
    template_name = "App/facilitators/list.html"

    def get_context_data(self, **kwargs):
        context = super(FacilitatorListView, self).get_context_data(**kwargs)
        context['link_name'] = 'facilitators-link'
        return context

class MoreMenuView(View):
    def get(self, request, year=None):
        # TODO add django filter to make a greater filtering system
        today = date.today()
        current_year = timezone.now().year
        
        days = Stat.objects.filter(date__year=current_year)
        # services = Service.objects.filter()
        
        highest_attendance = 0
        lowest_attendance = 1000
        highest_visitors = 0
        total_visitors = 0
        highest_salvations = 0
        total_salvations = 0
        
        highest_attendance_day = None
        lowest_attendance_day = None
        highest_visitors_day = None
        highest_salvations_day = None
        
        for day in days:
            attendance = day.totalAttendance()
            visitors = day.totalVisitors()
            salvations = day.totalSalvations()
            
            if attendance > highest_attendance:
                highest_attendance_day = day
                highest_attendance = attendance
            
            if attendance < lowest_attendance:
                lowest_attendance_day = day
                lowest_attendance = attendance
            
            if visitors > highest_visitors:
                highest_visitors_day = day
                highest_visitors = visitors
            
            if salvations > highest_salvations:
                highest_salvations_day = day
                highest_salvations = salvations
            
            total_visitors += visitors
            total_salvations += salvations
        
        template_name = "App/moremenu.html"
        context = {
            'year': today.year,
            'days': days,
            'highest_attendance_day': highest_attendance_day,
            'lowest_attendance_day': lowest_attendance_day,
            'highest_visitors_day': highest_visitors_day,
            'highest_salvations_day': highest_salvations_day,
            'total_visitors': total_visitors,
            'total_salvations': total_salvations,
        }
        return render(request, template_name, context)
    
def page_not_found(request, exception):
    return render(request, '404.html', status=404)

class AccessDeniedView(View):
    def get(self, request):
        template_name = "App/noaccess.html"
        context = {}
        return render(request, template_name, context)

class GeneralStatsView(View):
    def get(self, request, *args, **kwargs):
        today = date.today()
        day1 = today.replace(year=today.year,month=1,day=1)
        
        events = Stat.objects.filter(date__gte=day1)
        template_name = 'App/statistics.html'
        context = {}
        return render(request, template_name, context)
