from django.db import models


class GenderChoices(models.TextChoices):
    MALE = 'M', "Male"
    FEMALE = 'F', "Female"

# Create your models here.
class Facilitator(models.Model):
    name = models.CharField(max_length=25)
    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, null=True)
    only_in_band = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True)

    class Meta:
        verbose_name = 'Facilitator'
        verbose_name_plural = 'Facilitators'

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name
