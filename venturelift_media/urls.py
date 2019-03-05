from django.conf.urls import include, url
<<<<<<< HEAD
from .views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='homepage'),
    url(r'^stories/media/(?P<pk>\d+)/$',
        views.TextMediaView.as_view(), name='media_story'),
]
