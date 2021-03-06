from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from venturelift_profiles import views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^accounts/activate/complete/$',
        TemplateView.as_view(
            template_name='django_registration/activation_complete.html'
        ),
        name='django_registration_activation_complete'),
    # override the django_registration activation view
    url(r'^accounts/activate/(?P<activation_key>[-:\w]+)/$',
        views.ProfileActivationView.as_view(),
        name='django_registration_activate'),
    url(r'^accounts/', include('django_registration.backends.activation.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^profile/$', views.SummaryView.as_view(), name='profile_summary'),
    url(r'^supporter/list/$', views.SupporterView.as_view(), name='supporter_list'),
    url(r'^supporter/list/filter/(?P<supporter_type>[\w ]+)/$',
        views.SupporterFilterView.as_view(), name='supporter_filter'),
    url(r'^business/list/$', views.BusinessView.as_view(), name='business_list'),
    url(r'^business/list/startup/$',
        views.BusinessStartupView.as_view(), name='business_startup'),
    url(r'^business/list/smes/$',
        views.BusinessSMEView.as_view(), name='business_smes'),
    url(r'^investor/list/$', views.InvestorView.as_view(), name='investor_list'),
    url(r'^investor/list/filter/(?P<investor_type>[\w ]+)/$',
        views.InvestorFilterView.as_view(), name='investor_filter'),
    url(r'^supporter/follow/(?P<pk>\d+)/$',
        views.SupporterView.as_view(), name='supporter_follow'),
    url(r'^supporter/unfollow/(?P<pk>\d+)/$',
        views.SupporterView.as_view(), name='supporter_unfollow'),

    url(r'^business/follow/(?P<pk>\d+)/$',
        views.BusinessView.as_view(), name='business_follow'),

    url(r'^business/unfollow/(?P<pk>\d+)/$',
        views.BusinessView.as_view(), name='business_unfollow'),

    url(r'^investor/follow/(?P<pk>\d+)/$',
        views.InvestorView.as_view(), name='investor_follow'),

    url(r'^investor/unfollow/(?P<pk>\d+)/$',
        views.InvestorView.as_view(), name='investor_unfollow'),

    url(r'^business/profile/(?P<pk>\d+)/$',
        views.BusinessProfileView.as_view(), name='business_profile'),

    url(r'^supporter/profile/(?P<pk>\d+)/$',
        views.SupporterProfileView.as_view(), name='supporter_profile'),

    url(r'^investor/profile/(?P<pk>\d+)/$',
        views.InvestorProfileView.as_view(), name='investor_profile'),

    url(r'^oauth/', include('social_django.urls', namespace='social')),

    url(r'^post-like/(?P<pk>\d+)/$', views.SummaryView.as_view(), name='like_post'),
    url(r'^post-dislike/(?P<pk>\d+)/$',
        views.SummaryView.as_view(), name='dislike_post'),
    url(r'^create-business/step-1/$', views.CreateBusinessView.as_view(),
        name='create_business_step1'),
    url(r'^create-business/step-1/(?P<pk>\d+)/$',
        views.UpdateBusinessView.as_view(), name='update_business_step1'),
    url(r'^create-business/step-2/(?P<pk>\d+)/$',
        views.UpdateBusinessView.as_view(), name='update_business_step2'),
    url(r'^create-business/step-3/(?P<pk>\d+)/$',
        views.UpdateBusinessView.as_view(), name='update_business_step3'),
    url(r'^create-business/step-4/(?P<pk>\d+)/$',
        views.UpdateBusinessView.as_view(), name='update_business_step4'),
    url(r'^create-business/step-5/(?P<pk>\d+)/$',
        views.UpdateBusinessView.as_view(), name='update_business_step5'),
    url(r'^create-business/step-6/(?P<pk>\d+)/$',
        views.UpdateBusinessView.as_view(), name='update_business_step6'),
    url(r'^create-business/step-7/(?P<pk>\d+)/$',
        views.UpdateBusinessView.as_view(), name='update_business_step7'),
    url(r'^profile-create/$', views.ProfileCreateView.as_view(), name='profile_create'),
    url(r'^supporter-create/$', views.CreateSupporterView.as_view(),
        name='supporter_create'),
    url(r'^supporter-create/step-1/(?P<pk>\d+)/$', views.SupporterUpdateProfileView.as_view(),
        name='update_supporter_step1'),
    url(r'^supporter-create/step-2/(?P<pk>\d+)/$', views.SupporterUpdateProfileView.as_view(),
        name='update_supporter_step2'),
    url(r'^new-document-upload/$', views.CreateBlogPostView.as_view(), name='new_blog_post'),
    url(r'^investor-create/$', views.CreateInvestorView.as_view(),
        name='investor_create'),
    url(r'^investor-create/step-1/(?P<pk>\d+)/$',
        views.InvestorUpdateProfileView.as_view(), name='update_investor_step1'),
    url(r'^investor-create/step-2/(?P<pk>\d+)/$',
        views.InvestorUpdateProfileView.as_view(), name='update_investor_step2'),
    # url(r'^account_activation/$',
    #    views.VerificationAccountWaiting.as_view(), name='account_verification_waiting'),
]


