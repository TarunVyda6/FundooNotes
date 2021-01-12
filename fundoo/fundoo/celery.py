import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoo.settings')

app = Celery('fundoo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()