# tasks.py

from celery import shared_task
from django.contrib.auth.models import Group, Permission

@shared_task(bind=True)
def addPermissionToGroup(self, permission_id, group_name):
    try:
        permission = Permission.objects.get(id=permission_id)
        group = Group.objects.get(name=group_name)
        group.permissions.add(permission)
        group.save()
        return f"Permission {permission} add to group {group}"
    except Exception as e:
        return f"Error add permission: {e}"



@shared_task(bind=True)
def removePermissionFromGroup(self, permission_id, group_name):
    try:
        permission = Permission.objects.get(id=permission_id)
        group = Group.objects.get(name=group_name)
        group.permissions.remove(permission)
        group.save()
        return f"Permission {permission} removed from group {group}"
    except Exception as e:
        return f"Error removing permission: {e}"