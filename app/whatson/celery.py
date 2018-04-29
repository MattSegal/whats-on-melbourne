import os
from celery import Celery
from django.conf import settings

celery_host = os.environ.get('CELERY_HOST')
app = Celery('whatson', broker='redis://{}:6379'.format(celery_host))
app.config_from_object('django.conf:settings', namespace='CELERY')

