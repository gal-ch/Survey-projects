from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Job(models.Model):
    text = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    flagged = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return self.text


class Location(models.Model):
    name = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    flagged = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return self.name

class Employer(models.Model):
    name = models.CharField(max_length=250)
    location = models.ForeignKey(Location,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

