import calendar
from collections import OrderedDict, defaultdict
from datetime import date, datetime
import json

from django.db.models import OuterRef, Subquery
from django.http import QueryDict
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from App.mixins import RedirectNonStaffMixin
from django.utils import timezone

from Stat.models import Service, Stat
from facilitators.forms import FacilitatorForm
from facilitators.models import Facilitator, Tag

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
        facilitators = context['facilitators']

        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        selected_tags = self.request.GET.getlist('tag')

        context['active_count'] = facilitators.filter(active=True).count()
        context['inactive_count'] = facilitators.filter(active=False).count()
        context['served_count'] = facilitators.exclude(last_service_date__isnull=True).count()
        context['never_served_count'] = facilitators.filter(last_service_date__isnull=True).count()
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['search_query'] = self.request.GET.get('search', '').strip()
        context['tags'] = Tag.objects.all().order_by('name')
        context['selected_tags'] = selected_tags
        context['bulk_notice'] = self.request.GET.get('bulk_notice', '')
        return context
    
    def get_queryset(self):
        latest_service_date = Subquery(
            Service.objects.filter(
                facilitators_available=OuterRef('pk')
            ).order_by('-stat__date').values('stat__date')[:1]
        )

        qs = super().get_queryset().annotate(
            last_service_date=latest_service_date
        ).prefetch_related('tags').order_by('name')

        return self.apply_filters(qs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('App:access-denied')

        action = request.POST.get('bulk_action', '').strip()
        selected_ids = request.POST.getlist('facilitator_ids')

        if not selected_ids:
            return self.bulk_redirect('select_at_least_one')

        selected_facilitators = Facilitator.objects.filter(pk__in=selected_ids)

        if action == 'activate':
            selected_facilitators.update(active=True)
            return self.bulk_redirect('activated')

        if action == 'deactivate':
            selected_facilitators.update(active=False)
            return self.bulk_redirect('deactivated')

        if action == 'edit':
            if selected_facilitators.count() != 1:
                return self.bulk_redirect('select_one_for_edit')
            facilitator = selected_facilitators.first()
            return redirect(reverse('App:facilitator-update', kwargs={'pk': facilitator.pk}))

        return self.bulk_redirect('invalid_action')

    def apply_filters(self, facilitators):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search = self.request.GET.get('search', '').strip()
        selected_tags = self.request.GET.getlist('tag')

        if search:
            facilitators = facilitators.filter(name__icontains=search)

        if selected_tags:
            facilitators = facilitators.filter(tags__id__in=selected_tags).distinct()

        if start_date or end_date:
            facilitators = self.filter_by_active_dates(facilitators, start_date, end_date)

        return facilitators

    def bulk_redirect(self, notice):
        base_url = reverse('App:facilitator-list')
        return_query = self.request.POST.get('return_query', '').strip()
        params = QueryDict(return_query, mutable=True)
        params['bulk_notice'] = notice
        query_string = params.urlencode()

        if query_string:
            return redirect(f"{base_url}?{query_string}")

        return redirect(base_url)
    
    def filter_by_active_dates(self, facilitators, start_date, end_date):
        stats = Stat.objects.all()

        if start_date:
            stats = stats.filter(date__gte=start_date)

        if end_date:
            stats = stats.filter(date__lte=end_date)

        facilitator_ids = Service.objects.filter(
            stat__in=stats,
            facilitators_available__isnull=False,
        ).values_list('facilitators_available__id', flat=True)

        return facilitators.filter(pk__in=facilitator_ids).distinct()


class MoreMenuView(View):
    def get(self, request, year=None):
        template_name = "App/moremenu.html"
        context = {}
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
    
