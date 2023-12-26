from django.db import models

# Create your models here.
class Event(models.Model):
    class STATUSES(models.TextChoices):
        PLANNED = (0, "Planned")
        CANCELLED = (1, "Cancelled")
        POSTPONED = (2, "Postponed")
        NODATE = (3, "No date yet")
        
    name = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=50, blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUSES.choices, default=STATUSES.PLANNED)
    details = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
