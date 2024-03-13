# tasks.py

from celery import shared_task
from django.contrib.auth.models import Group, Permission

@shared_task(bind=True)
def addPermissionToGroup(self, permission_id, group_name):
    permission = Permission.objects.get(codename='add_project', content_type__app_label='showcase_projects')
    group = Group.objects.get(name='student')
    group.permissions.add(permission)
    group.save()



#   Короче, надо попробывать вынести базу данных в docker контейнер
#   потому что worker видит, но не может заносить в нее данные
#   лучше вообще перейти на MySQL!!!
