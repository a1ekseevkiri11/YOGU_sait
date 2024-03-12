# from django.contrib.auth.models import Group
# from .models import TimePermission
# from celery import shared_task
# from django.utils import timezone
# from .models import TimePermission

# @shared_task
# def check_permissions():
#     now = timezone.now()
#     time_permissions = TimePermission.objects.filter(start_time__lte=now, end_time__gte=now)
    
#     for time_permission in time_permissions:
#         if time_permission.is_active():
#             group = Group.objects.get(name='student')
#             group.permissions.add(time_permission.permission)
#         else:
#             group = Group.objects.get(name='student')
#             group.permissions.remove(time_permission.permission)