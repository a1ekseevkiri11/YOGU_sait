# tasks.py

from celery import shared_task
from django.contrib.auth.models import Group, Permission

@shared_task(bind=True)
def addPermissionToGroup(self, permission_id, group_name):
    permission = Permission.objects.get(id=permission_id)
    group = Group.objects.get(name=group_name)
    group.permissions.add(permission)
    group.save()
