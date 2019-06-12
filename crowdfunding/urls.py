from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from crowdfunding import views

app_name = 'crowdfunding'
urlpatterns = [
    # ex: /crowdfunding/
    url(r'^$', views.index, name='index'),
    url(r'^business/(?P<campaign_id>[0-9]+)/$', views.business_campaign_view, name='business_campaign_view'),
    url(r'^create_campaign/$', views.CreateCampaignView.as_view(), name='create_campaign'),
    url(r'^create_donation/(?P<campaign_id>[0-9]+)/$', views.create_donation, name='create_donation'),
    url(r'^make_payment/$', views.make_payment, name='make_payment'),
    url(r'^filter_campaign/$', views.filter_campaign_view, name='filter_campaign'),
]