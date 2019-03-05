from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='homepage'),
    url(r'^stories/(?P<pk>\d+)/$', StoryDetailView.as_view(), name='story_detail'),
]