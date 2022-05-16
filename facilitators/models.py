from django.db import models

# Create your models here.
class Facilitator(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

class PrayerRequest(models.Model):
    facilitator = models.ForeignKey(Facilitator, on_delete=models.SET_NULL, null=True, related_name='prayer_requests')
    prayer_request = models.TextField()
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.facilitator.name