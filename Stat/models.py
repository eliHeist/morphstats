from django.db import models 
from django.db.models import Sum

from facilitators.models import Facilitator

# Create your models here.
class Stat(models.Model):
    title = models.CharField(max_length=50, default='Sunday Celebration Services', blank=True)
    date = models.DateField(unique=True)
    comments = models.TextField(blank=True, null=True)

    def formatedDate(self):
        return self.date.strftime("%A, %d %B %Y")
    
    def totalAttendance(self):
        count:int = 0
        for service in self.services.all():
            count += service.totalMorphers()
        return count
    
    def totalJunior(self):
        return self.services.aggregate(total=Sum('junior'))['total'] or 0

    def totalSenior(self):
        return self.services.aggregate(total=Sum('senior'))['total'] or 0

    def totalSalvations(self):
        return self.services.aggregate(total=Sum('salvations'))['total'] or 0

    def totalVisitors(self):
        return self.services.aggregate(total=Sum('first_time_visitors'))['total'] or 0
    
    def facilitators(self):
        # Returns distinct Facilitator queryset instead of a raw Python list
        return Facilitator.objects.filter(
            services_served__stat=self
        ).distinct()
    
    def facilitatorsData(self):
        facilitators_dict = {}

        for service in self.services.all():
            for facilitator in service.facilitators_available.all():
                if facilitator.pk not in facilitators_dict:
                    facilitators_dict[facilitator.pk] = {
                        'facilitator': facilitator,
                        'service_count': 1
                    }
                else:
                    facilitators_dict[facilitator.pk]['service_count'] += 1

        return list(facilitators_dict.values())

    
    def facilitatorsCount(self):
        facilitators_list = []
        for service in self.services.all():
            for facilitator in service.facilitators_available.all():
                if facilitator not in facilitators_list:
                    facilitators_list.append(facilitator)
        return len(facilitators_list)
    
    def total_that_served(self):
        total = 0
        for service in self.services.all():
            if service.non_system_facilitators and service.non_system_facilitators > total:
                total = service.non_system_facilitators
        
        total += self.facilitatorsCount()
        
        return total
    
    def totals(self):
        male = 0
        female = 0
        f_list = self.facilitators()

        for f in f_list:
            if f.gender == "M":
                male+=1
            elif f.gender == "F":
                female+=1
        
        return {
            "male": male,
            "female": female,
            "total": male + female,
        }

    def __str__(self):
        return str(self.date.strftime("%A, %d %B %Y"))


class Service(models.Model):
    SERVICES = (
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
    )
    stat = models.ForeignKey('Stat', on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=20, choices=SERVICES)
    junior = models.SmallIntegerField(blank=True, null=True)
    senior = models.SmallIntegerField(blank=True, null=True)
    first_time_visitors = models.PositiveSmallIntegerField(blank=True, null=True)
    salvations = models.PositiveSmallIntegerField(blank=True, null=True)
    facilitators = models.PositiveSmallIntegerField(blank=True, null=True)
    non_system_facilitators = models.PositiveSmallIntegerField(blank=True, null=True)
    facilitators_available = models.ManyToManyField(Facilitator, blank=True, related_name='services_served')

    fixed_total = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.stat}: {self.name}'
    
    def totalMorphers(self):
        if self.fixed_total:
            return self.fixed_total

        return (self.junior or 0) + (self.senior or 0) 
    
    def syncFacilitators(self):
        self.facilitators = self.facilitators_available.count()


