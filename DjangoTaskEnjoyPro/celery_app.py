import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoTaskEnjoyPro.settings')

app = Celery('DjangoTaskEnjoyPro', broker='amqp://user:pass@rabbitmq:5672')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
