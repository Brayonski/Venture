from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import include, url

urlpatterns = [
    url(r'^accounts/', include('django_registration.backends.activation.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]