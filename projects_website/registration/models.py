from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

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
    if hasattr(instance, 'lecturer'):
        instance.lecturer.save()
    if hasattr(instance, 'customer'):
        instance.customer.save()


class Student(Profile):
    pass


class Lecturer(Profile):
    pass


class Customer(Profile):
    pass