from django.db import models
from facilitators.models import Facilitator
from morphers.models import Morpher


# Create your models here.
class Day(models.Model):
    title = models.CharField(max_length=50, default='Sunday Service', blank=True)
    date = models.DateField(unique=True)
    comments = models.TextField(blank=True, null=True)
    facilitators = models.ManyToManyField(Facilitator, related_name='days')

    def __str__(self):
        return str(self.date.strftime("%A, %d %B %Y"))


class Service(models.Model):
    SERVICES = (
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
    )
    date = models.ForeignKey('Day', on_delete=models.DO_NOTHING, related_name='services')
    service = models.CharField(max_length=5, choices=SERVICES)
    first_time_visitors = models.ManyToManyField(Morpher, blank=True)

    def __str__(self):
        return f'{self.date}: {self.service}'
    

class Group(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, related_name='small_groups')
    morphers = models.ManyToManyField(Morpher, related_name='services_attended')
    facilitators = models.ManyToManyField(Facilitator)
    salvations = models.ManyToManyField(Morpher, blank=True)

    def __str__(self):
        return f'{self.service}: Group'