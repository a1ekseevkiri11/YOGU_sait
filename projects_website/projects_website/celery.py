import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projects_website.settings')

app = Celery('projects_website',)
app.conf.broker_url = 'redis://redis:6379/0'

app.autodiscover_tasks()



