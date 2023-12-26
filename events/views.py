from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from datetime import date
from events.forms import EventModelForm

from events.models import Event

# Create your views here.
class CalendarView(View):
    def get(self, request, *args, **kwargs):
        events = Event.objects.all().order_by('date')
        # events = Event.objects.filter(date__gte=date.today())
        print(events)
        template_name = 'events/calendar.html'
        context = {
            'events': events
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
        if pk:
            instance = Event.objects.get(pk=pk)
        else:
            instance = None
            
        context = {
            'instance': instance,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk=None):
        print('\npost\n')
        data = request.POST
        print(data)
        if pk:
            event = Event.objects.get(pk=pk)
            event.name = data['name']
            event.date = data['date']
            event.venue = data['venue']
            event.status = data['status']
            event.details = data['details']
        else:
            event = Event(
                name=data['name'],
                date=data['date'],
                venue=data['venue'],
                status=data['status'],
                details=data['details'],
            )
        
        if event.save():
            return redirect(reverse_lazy('events:detail', kwargs={'pk':event.pk}))
        else:
            context = {
                'instance': event,
            }
            return render(request, self.template_name, context)
