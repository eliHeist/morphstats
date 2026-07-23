from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from Stat.models import Stat
from facilitators.models import Facilitator

class AttendanceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # 1. Parse date parameters
        from_date_str = request.GET.get('from_date', '').strip()
        to_date_str = request.GET.get('to_date', '').strip()

        today = timezone.now().date()

        # Parse 'to_date' (Default: today)
        if to_date_str:
            try:
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
            except ValueError:
                to_date = today
                to_date_str = today.strftime('%Y-%m-%d')
        else:
            to_date = today
            to_date_str = today.strftime('%Y-%m-%d')

        # Parse 'from_date' (Default: 90 days prior to to_date)
        if from_date_str:
            try:
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            except ValueError:
                from_date = to_date - timedelta(days=90)
                from_date_str = from_date.strftime('%Y-%m-%d')
        else:
            from_date = to_date - timedelta(days=90)
            from_date_str = from_date.strftime('%Y-%m-%d')

        # 2. Fetch Stat objects for the date range using pure date objects
        days = Stat.objects.filter(
            date__gte=from_date,
            date__lte=to_date
        ).order_by('-date')

        facilitators = Facilitator.objects.filter(active=True).order_by('name')

        # 3. OPTIMIZED LOOKUP (Fixed 'service' reverse relation name):
        attendance_records = Stat.objects.filter(
            id__in=[stat.id for stat in days]
        ).values_list('id', 'services__facilitators_available__id')

        # Build lookup set: {(stat_id, facilitator_id), ...}
        attended_set = {
            (stat_id, facilitator_id)
            for stat_id, facilitator_id in attendance_records
            if facilitator_id is not None
        }

        # 4. Construct matrix rows
        class FacilitatorAttendanceRow:
            def __init__(self, facilitator, statuses):
                self.facilitator = facilitator
                self.statuses = statuses

        facilitator_rows = []
        for facilitator in facilitators:
            statuses = [
                (stat.id, facilitator.id) in attended_set
                for stat in days
            ]
            facilitator_rows.append(FacilitatorAttendanceRow(facilitator, statuses))

        template_name = "facilitators/attendance.html"
        context = {
            'days': days,
            'facilitator_rows': facilitator_rows,
            'from_date': from_date_str,
            'to_date': to_date_str,
        }
        return render(request, template_name, context)