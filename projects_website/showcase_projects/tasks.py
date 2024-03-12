# tasks.py

from celery import shared_task
from django.utils import timezone
from .models import TimePermission
from django.contrib.auth.models import Group

@shared_task
def check_permissions():
    now = timezone.now()
    timePermissions = TimePermission.objects.filter(start_time__lte=now, end_time__gte=now)
    
    for timePermission in timePermissions:
        if timePermission.is_active():
            group = Group.objects.get(name='student')
            group.permissions.add(timePermission.permission)
        else:
            group = Group.objects.get(name='student')
            group.permissions.remove(timePermission.permission)
