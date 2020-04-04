"""
WSGI config for venturelift_cms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('F:\work\backup\otbafrica-venturelift-5ee3402e7447\venturelift_cms\settings.py')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "venturelift_cms.settings")

application = get_wsgi_application()
