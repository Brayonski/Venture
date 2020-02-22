from django.conf.urls import include, url
from venturelift_media import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='homepage'),
    url(r'^stories/media/(?P<pk>\d+)/$', views.TextMediaView.as_view(), name='media_story'),
    url(r'^videos/(?P<name>\w+)/$', views.HomeView.as_view(), name='media_videos'),
    url(r'^podcast/(?P<name>\w+)/$', views.HomeView.as_view(), name='media_podcast'),
]
