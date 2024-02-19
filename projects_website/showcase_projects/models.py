from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .permission import(
    canAddParticipation,
    canAddProject
)


class Project(models.Model):
    title = models.CharField(max_length=100)
    place = models.IntegerField(default=0)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def freePlaces(self):
        return self.place > self.participation_set.count()

    def studentInThisProject(self, user):
        return self.participation_set.filter(student=user).exists()

    def addStudent(self, user):
        if not canAddParticipation(user):
            return

        if Participation.studentInProject(user):
            return

        if not self.freePlaces():
            return

        Participation.objects.create(project=self, student=user)

    def __str__(self):
        return self.title
    


class Participation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def studentInProject(student):
        return Participation.objects.filter(student=student).exists()
    

