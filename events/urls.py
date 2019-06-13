from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import include, url
from events import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(),
        name='events_home'),
    url(r'^-content/(?P<pk>\d+)/$',
        views.SingleEventView.as_view(), name='event_view_content'),
    url(r'^-content/filter/(?P<pk>\d+)/$',
        views.EventFilterView.as_view(), name='event_view_content_filter'),
]
