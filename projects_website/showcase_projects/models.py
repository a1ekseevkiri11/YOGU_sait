from django.db import models
from registration.models import Profile

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


    def addLetter(self, student, letter):
        if Participation.objects.filter(student=student).exists():
            return

        if MotivationLetters.objects.filter(student=student).exists():
            return
        
        MotivationLetters.objects.create(project=self, student=student, letter=letter)


    def addRejectionComment(self, comment):
        if comment != '':
            RejectionComment.objects.create(project=self, comment=comment)

    def __str__(self):
        return self.title
    


class Participation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.OneToOneField(Profile, on_delete=models.CASCADE)
    

class MotivationLetters(ModelWithStatus):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    letter = models.FileField(upload_to='letters/')


class RejectionComment(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='rejection_comment')
    comment = models.TextField()