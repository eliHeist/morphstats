from django.db import models

# Create your models here.
class Morpher(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20, blank=True, null=True)
    parents_contact = models.CharField(max_length=20, blank=True, null=True)
    grade = models.ForeignKey("Grade", on_delete=models.SET_NULL, blank=True, null=True, related_name="morphers")
    residence = models.ForeignKey("Residence", on_delete=models.SET_NULL, blank=True, null=True, related_name="morphers")
    school = models.ForeignKey("School", on_delete=models.SET_NULL, blank=True, null=True, related_name="morphers")

    def __str__(self):
        return self.name


class Residence(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField( max_length=10)
    level = models.ForeignKey('Level', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField( max_length=10)

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    
    