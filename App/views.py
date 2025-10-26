import calendar
from collections import OrderedDict, defaultdict
from datetime import date, datetime
import json

from django.shortcuts import get_object_or_404, render, redirect
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
    template_name = 'App/stats-detail-new.html'
    context_object_name = 'stat'

class LatestStatDetailView(TemplateView):
    template_name = 'App/stats-detail-new.html'
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
    def get(self, request, pk=None):
        if pk is None:
            stat = Stat.objects.all().order_by('-date').first()
        else:
            stat = Stat.objects.get(pk=pk)
        context = {
            'stat': stat,
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

        # get the start and end dates from the request
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date or end_date:
            context['facilitators'] = self.filter_by_active_dates(context['facilitators'], start_date, end_date)

        context['active_count'] = context['facilitators'].filter(active=True).count()
        context['inactive_count'] = context['facilitators'].filter(active=False).count()
        context['start_date'] = start_date
        context['end_date'] = end_date
        return context
    
    def get_queryset(self):
        qs = super().get_queryset().order_by('name')
        return qs 
    
    def filter_by_active_dates(self, facilitators, start_date, end_date):

        stats = Stat.objects.filter(date__gte=start_date, date__lte=end_date)

        facilitators_set = set()
        for stat in stats:
            for service in stat.services.all():
                facilitator_ids = service.facilitators_available.all().values_list('id', flat=True)
                facilitators_set.update(facilitator_ids)
        
        filtered = facilitators.filter(pk__in=facilitators_set)

        return filtered


class MoreMenuView(View):
    def get(self, request, year=None):
        # TODO add django filter to make a greater filtering system
        today = date.today()
        current_year = timezone.now().year
        
        days = Stat.objects.filter(date__year=current_year).order_by('-date')
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


class FacilitatorDetailView(View):
    class PairSet:
        def __init__(self, stat=None, status=None) -> None:
            self.stat = stat
            self.status = status

    def get(self, request, pk, *args, **kwargs):
        template_name = 'App/facilitators/facilitator-calendar.html'
        stats = Stat.objects.filter(date__year=datetime.now().year).order_by('date')
        facilitator = get_object_or_404(Facilitator, pk=pk)

        # Daily stats (already ordered by date)
        main_list = []
        for stat in stats:
            mini_list = self.PairSet(stat)
            mini_list.status = facilitator in stat.facilitators()
            main_list.append(mini_list)

        # Build monthly stats
        monthly_stats = OrderedDict()
        for month_num in range(1, 13):
            month_name = calendar.month_abbr[month_num]
            monthly_stats[month_name] = {"month": month_name, "days_present": 0}

            month_stats = stats.filter(date__month=month_num)
            for stat in month_stats:
                if facilitator in stat.facilitators():
                    monthly_stats[month_name]["days_present"] += 1

        context = {
            'facilitator': facilitator,
            'list': main_list,
            'monthly_stats': json.dumps(monthly_stats)
        }
        return render(request, template_name, context)
    
