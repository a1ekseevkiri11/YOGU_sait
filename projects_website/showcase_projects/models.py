from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from registration.models import(
    Student,
    Customer,
    Lecturer,
)



class Project(models.Model):
    title = models.CharField(max_length=100)
    place = models.IntegerField(default=6)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def freePlaces(self):
        return self.place > self.participation_set.count()

    def studentInThisProject(self, student):
        return self.participation_set.filter(student=student).exists()

    def addStudent(self, student):
        
        if Participation.objects.filter(student=student).exists():
            return

        if not self.freePlaces():
            return

        Participation.objects.create(project=self, student=student)

    def __str__(self):
        return self.title
    



class Participation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)




class MotivationLetters(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    letter = models.FileField(upload_to='letters/')


