from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from datetime import date
from django.db import models

from events.models import Event

# Create your views here.
class CalendarView(View):
    def get(self, request, *args, **kwargs):
        # events = Event.objects.all().order_by('date')
        ongoing_events = Event.objects.filter(
            models.Q(end_date__gte=date.today()) | models.Q(start_date__gte=date.today())
        )
        template_name = 'events/calendar.html'
        context = {
            'events': ongoing_events
        }
        return render(request, template_name, context)

class EventDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        template_name = 'events/detail.html'
        event = Event.objects.get(pk=pk)
        context = {
            'event': event,
        }
        return render(request, template_name, context)

class EventCreateUpdateView(View):
    template_name = 'events/create-update.html'
    def get(self, request, pk=None, *args, **kwargs):
        instance = Event.objects.get(pk=pk) if pk else None
        context = {
            'instance': instance,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk=None):
        print('\npost\n')
        data = request.POST
        print(data)
        if pk:
            event = self._extracted_from_post(pk, data)
        else:
            event = Event(
                name=data['name'],
                start_date=data['start_date'],
                end_date=data['end_date'] if data['end_date'] else None,
                venue=data['venue'],
                status=data['status'],
                details=data['details'],
            )

        event.save()
        print('\nSaved\n')
        return redirect(reverse_lazy('events:detail', kwargs={'pk':event.pk}))
        # print('\nSaved Alt\n')
        # print(event.errors)
        # context = {
        #     'instance': event,
        # }
        # return render(request, self.template_name, context)

    # TODO Rename this here and in `post`
    def _extracted_from_post(self, pk, data):
        result = Event.objects.get(pk=pk)
        result.name = data['name']
        result.start_date = data['start_date']
        result.end_date = data['end_date'] if data['end_date'] else None
        result.venue = data['venue']
        result.status = data['status']
        result.details = data['details']
        return result
