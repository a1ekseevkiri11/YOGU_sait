from django.db import models
from registration.models import Profile
from django.contrib.auth.models import Permission
from django.utils import timezone

from .tasks import (
    addPermissionToGroup,
    removePermissionFromGroup,
)

class ModelWithStatus(models.Model):

    class Meta:
        abstract = True
    
    STATUS_CHOICES = [
        ('accepted', 'Принят'),
        ('processing', 'В обработке'),
        ('rejected', 'Отклонен'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def set_status(self, new_status):
        self.status = new_status
        self.save()
            
    def get_status(self):
        return self.status



class Project(ModelWithStatus):
    class Meta:
        permissions = [
            ("change_status_project", "Can change status project"),
        ]
    title = models.CharField(max_length=100)
    place = models.IntegerField(default=6)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='customer')
    lecturer = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='lecturer')

    
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

    def deleteStudent(self, student):
        try:
            participation = Participation.objects.get(project=self, student=student)
            participation.delete()
        except Participation.DoesNotExist:
            pass

    def addLetter(self, student, letter):
        if Participation.objects.filter(student=student).exists():
            return

        if MotivationLetters.objects.filter(student=student).exists():
            return
        
        MotivationLetters.objects.create(project=self, student=student, letter=letter)

    def addRejectionComment(self, comment):
        if comment != '':
            RejectionComment.objects.create(project=self, comment=comment)

    def deleteRejectionComment(self):
        try:
            comment = RejectionComment.objects.get(project=self)
            comment.delete()
        except RejectionComment.DoesNotExist:
            pass

    def __str__(self):
        return self.title
    


class Participation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.OneToOneField(Profile, on_delete=models.CASCADE)
    

class MotivationLetters(ModelWithStatus):

    class Meta:
        permissions = [
            ("download_motivationletters", "Can download motivation letters"),
            ("change_status_motivationletters", "Can change status motivation letters"),
        ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    letter = models.FileField(upload_to='letters/')


class RejectionComment(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='rejection_comment')
    comment = models.TextField()


class TimePermission(models.Model):

    class Meta:
        unique_together = ('permission', 'operation')


    OPERATION_CHOICES = (
        ('add', 'Add'),
        ('delete', 'Delete'),
    )

    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    time = models.DateTimeField()
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES, blank=True, null=True)
    task_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.operation == 'add':
            task = addPermissionToGroup.delay(self.permission.pk, "student")
            self.task_id = task.id
        elif self.operation == 'delete':
            task = removePermissionFromGroup.delay(self.permission.pk, "student")
            self.task_id = task.id
        return super().save(*args, **kwargs)