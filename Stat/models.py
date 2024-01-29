from django.db import models 
import datetime

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
    
    def totalSalvations(self):
        count:int = 0
        for service in self.services.all():
            if service.salvations:
                count += service.salvations
        return count
    
    def totalVisitors(self):
        count:int = 0
        for service in self.services.all():
            if service.first_time_visitors:
                count += service.first_time_visitors
        return count
    
    def facilitators(self):
        facilitators_list = []
        for service in self.services.all():
            for facilitator in service.facilitators_available.all():
                if facilitator not in facilitators_list:
                    facilitators_list.append(facilitator)
        return facilitators_list

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
    facilitators_available = models.ManyToManyField(Facilitator, blank=True)

    def __str__(self):
        return f'{self.stat}: {self.name}'
    
    def totalMorphers(self):
        count = 0
        if self.junior:
            count += self.junior
        if self.senior:
            count += self.senior
        return count
    
    def syncFacilitators(self):
        self.facilitators = self.facilitators_available.count()


