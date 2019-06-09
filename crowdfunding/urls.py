from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from crowdfunding import views

app_name = 'crowdfunding'
urlpatterns = [
    # ex: /crowdfunding/
    url(r'^$', views.index, name='index'),
    url(r'^business/(?P<campaign_id>[0-9]+)/$', views.business_campaign_view, name='business_campaign_view'),
    url(r'^create_campaign/$', views.create_campaign, name='create_campaign'),
]