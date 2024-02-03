from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from Stat.models import Stat

from facilitators.models import Facilitator

# Create your views here.
class AttendanceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        arguments = args
        print(arguments)

        current_year = timezone.now().year
        # Calculate the date 3 months ago from today
        three_months_ago = datetime.now() - timedelta(days=90)

        facilitators = Facilitator.objects.filter(active=True).order_by('name')

        # days = Stat.objects.filter(date__year=current_year).order_by('-date')
        days = Stat.objects.filter(date__gte=three_months_ago).order_by('-date')



        class StatPair:
            def __init__(self, stat=None, data=None) -> None:
                if data is None:
                    data = []
                self.stat = stat
                self.data = data


        calendar = []
        for stat in days:
            pair = StatPair(stat, [])
            print(pair.data)
            for facilitator in facilitators:
                if facilitator in stat.facilitators():
                    pair.data.append(True)
                else:
                    pair.data.append(False)
            print(pair.data)
                # print(f'{pair.stat} - {facilitator}')
            calendar.append(pair)

        template_name = "facilitators/attendance.html"
        context = {
            'calendar': calendar,
            'facilitators': facilitators,
        }
        return render(request, template_name, context)
