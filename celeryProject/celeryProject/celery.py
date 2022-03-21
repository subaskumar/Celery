# This module that defines the Celery instance

import os
from celery import Celery
from django.conf import settings

# we set the default DJANGO_SETTINGS_MODULE environment variable for the celery command-line progra
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celeryProject.settings')

app = Celery('celeryProject')


# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings',namespace='CELERY')

# Celery will automatically discover tasks from all registered Django apps( installed app).
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))