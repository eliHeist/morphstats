from datetime import timedelta
from django.shortcuts import render
from django.views.generic import ListView
from morphers.models import Level

from stats.models import Day, Service

# utility classes
class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return self.count

    def decrement(self):
        self.count -= 1
        return self.count

    def double(self):
        self.count *= 2
        return self.count



# Day Views
def getPresent(day):
    morphers = []
    for service in day.services.all():
        for group in service.small_groups.all():
            for morpher in group.morphers.all():
                if morpher not in morphers:
                    morphers.append(morpher)
    return morphers


def getAbsent(day):
    absent_morphers = []
    current_sunday = day.date
    previous_sunday = current_sunday - timedelta(7)
    if prev_day := Day.objects.filter(date=previous_sunday):
        p_day = prev_day.first()
    else:
        return absent_morphers

    current_morphers = getPresent(day)
    prev_morphers = getPresent(p_day)

    for morpher in prev_morphers:
        if morpher not in current_morphers and morpher not in absent_morphers:
            absent_morphers.append(morpher)
    return absent_morphers



def dayListView(request):
    days = Day.objects.all()
    template_name = "stats/days/list.html"
    context = {
        'days':days,
    }
    return render(request, template_name, context)

def dayDetailView(request, pk):
    day = Day.objects.get(id=pk)
    
    template_name = "stats/days/detail.html"

    context = {
        'day':day,
        'absent':getAbsent(day),
    }
    return render(request, template_name, context)

# service views
def serviceDetailView(request, pk):
    service = Service.objects.get(id=pk)
    counter = Counter()
    template_name = "stats/services/detail.html"
    context = {
        'service':service,
        'counter':counter,
    }
    return render(request, template_name, context)

# stats views
def getFacilitatorCount(service):
    return sum(group.facilitators.count() for group in service.small_groups.all())

def getCount(service, name):
    level = Level.objects.get(name=name)
    count = 0
    for group in service.small_groups.all():
        for morpher in group.morphers.all():
            if morpher and morpher.grade and morpher.grade.level == level:
                count+=1
    return count

def getSalvationsCount(service):
    return sum(group.salvations.count() for group in service.small_groups.all())

def statsView(request):
    days = Day.objects.all()[:10]
    template_name = "stats/stats.html"
    dayz = []

    for day in days:
        if day.services.all():
            dayz.append(day)
        else:
            day.comment = 'no morph services'

    for day in dayz:
        first_service = day.services.get(service='1st')
        second_service = day.services.get(service='2nd')
        third_service = day.services.get(service='3rd')
        # fomular
        # gotten
        day.third_facilitators = getFacilitatorCount(third_service)
        day.third_junior = getCount(third_service, 'Junior')
        day.third_senior = getCount(third_service, 'Senior')
        day.third_count = day.third_junior + day.third_senior
        day.third_salvations = getSalvationsCount(third_service)
        day.third_ftv = third_service.first_time_visitors.count()
        # gotten
        day.second_facilitators = getFacilitatorCount(second_service)
        day.second_junior = getCount(second_service, 'Junior')
        day.second_senior = getCount(second_service, 'Senior')
        day.second_count = day.second_junior + day.second_senior
        day.second_salvations = getSalvationsCount(second_service)
        day.second_ftv = second_service.first_time_visitors.count()
        # gotten
        day.first_facilitators = getFacilitatorCount(first_service)
        day.first_junior = getCount(first_service, 'Junior')
        day.first_senior = getCount(first_service, 'Senior')
        day.first_count = day.first_junior + day.first_senior
        day.first_salvations = getSalvationsCount(first_service)
        day.first_ftv = first_service.first_time_visitors.count()

    
    context = {
        'days':days,
    }
    return render(request, template_name, context)



