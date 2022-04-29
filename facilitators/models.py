from django.db import models

# Create your models here.
class Facilitator(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name