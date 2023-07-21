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
        return self.junior + self.senior
    
    def syncFacilitators(self):
        self.facilitators = self.facilitators_available.count()


