from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def assign_to_group(self):
        pass

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    if hasattr(instance, 'student'):
        instance.student.save()
    elif hasattr(instance, 'lecturer'):
        instance.lecturer.save()
    elif hasattr(instance, 'customer'):
        instance.customer.save()


class Student(Profile):

    def assign_to_group(self):
        group_name = 'student'
        group, created = Group.objects.get_or_create(name=group_name)
        self.user.groups.add(group)



class Lecturer(Profile):

    def assign_to_group(self):
        group_name = 'lecturer'
        group, created = Group.objects.get_or_create(name=group_name)
        self.user.groups.add(group)


class Customer(Profile):

    def assign_to_group(self):
        group_name = 'customer'
        group, created = Group.objects.get_or_create(name=group_name)
        self.user.groups.add(group)



class Project(models.Model):
    title = models.CharField(max_length=100)
    place = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

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