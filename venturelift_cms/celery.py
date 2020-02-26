from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venturelift_cms.settings')

from django.conf import settings

app = Celery('venturelift_cms')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks('settings.INSTALLED_APPS')

if __name__ == '__main__':
    app.start()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))