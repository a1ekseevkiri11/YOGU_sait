import os
import time

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projects_website.settings')

app = Celery('projects_website',)




app.autodiscover_tasks()
app.conf.broker_url = 'redis://localhost:6379/'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    time.sleep(20)
    print('Это работает!!')