from django.db import models

# Create your models here.
class Facilitator(models.Model):
    name = models.CharField(max_length=25)
    active = models.BooleanField(default=True)
    only_in_band = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Facilitator'
        verbose_name_plural = 'Facilitators'

    def __str__(self):
        return self.name
