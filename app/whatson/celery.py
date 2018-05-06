import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

HOUR = 60 * 60


celery_host = os.environ.get('CELERY_HOST')
app = Celery('whatson', broker='redis://{}:6379'.format(celery_host))
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    app.conf.beat_schedule = {
        'run-scrapers': {
            'task': 'whatson.tasks.run_scrapers',
            'schedule': HOUR,
        },
        'geocode-venues': {
            'task': 'whatson.tasks.geocode_venues',
            'schedule': HOUR - HOUR / 3,
        },
    }
