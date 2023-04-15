from django.db import models 
import datetime

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
    junior = models.SmallIntegerField(default=0)
    senior = models.SmallIntegerField(default=0)
    first_time_visitors = models.PositiveSmallIntegerField(default=0)
    salvations = models.PositiveSmallIntegerField(default=0)
    facilitators = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.stat}: {self.name}'
    
    def totalMorphers(self):
        return self.junior + self.senior