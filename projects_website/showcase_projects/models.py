from django.db import models
from registration.models import Profile



class Project(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Принят'),
        ('processing', 'В обработке'),
        ('rejected', 'Отклонен'),
    ]

    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
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

    def addLetter(self, student, letter_file):
        if Participation.objects.filter(student=student).exists():
            return

        if MotivationLetters.objects.filter(student=student).exists():
            return
        
        MotivationLetters.objects.create(project=self, student=student, letter=letter_file)

    def __str__(self):
        return self.title
    



class Participation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.OneToOneField(Profile, on_delete=models.CASCADE)



class MotivationLetters(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.OneToOneField(Profile, on_delete=models.CASCADE)
    letter = models.FileField(upload_to='letters/')


