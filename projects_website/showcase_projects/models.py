from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=100)
    place = models.IntegerField(default=0)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
