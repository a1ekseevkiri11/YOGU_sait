import os
from celery import Celery
from . import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projects_website.settings')

app = Celery('projects_website',)
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

app.autodiscover_tasks()



