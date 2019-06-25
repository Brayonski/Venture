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
    #url(r'^mpesa_lipa/$', views.get_mpesa_token, name='get_mpesa_token'),
    url(r'^mpesa_checkout_response/$', views.get_online_checkout_response, name='get_online_checkout_response'),
    url(r'^make_payment/$', views.make_payment, name='make_payment'),
    url(r'^filter_campaign/$', views.filter_campaign_view, name='filter_campaign'),

    #crowdfunder
    url(r'^crowdfunder/$', views.crowdfunderindex, name='crowdfunderindex'),
    url(r'^crowdfunder/filter_campaign/$', views.crowdfunder_filter_campaign_view, name='crowdfunder_filter_campaign'),
    url(r'^crowdfunder/create_donation/(?P<campaign_id>[0-9]+)/$', views.crowdfunder_create_donation, name='crowdfunder_create_donation'),
    url(r'^crowdfunder/make_payment/$', views.crowdfunder_make_payment, name='crowdfunder_make_payment'),
]