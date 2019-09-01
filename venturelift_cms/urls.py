# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from newsletter_subscription.backend import ModelBackend
from newsletter_subscription.urls import newsletter_subscriptions_urlpatterns
from venturelift_media.models import Subscription
from django_registration.backends.activation.views import RegistrationView
from django.views.generic import TemplateView
from venturelift_cms import views

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^profile/', include('venturelift_profiles.urls')),
    url(r'^crowdfunding/', include('crowdfunding.urls')),
    url(r'^knowledge-center/', include('knowledge_center.urls')),
    url(r'^events', include('events.urls')),
    url(r'^registration/', RegistrationView.as_view(), name='registration_in'),
    url(r'^newsletter/', include(newsletter_subscriptions_urlpatterns(backend=ModelBackend(Subscription),))),
    url(r'^$', TemplateView.as_view(template_name="landing.html")),
    url(r'^about-us/', TemplateView.as_view(template_name="page_about_us.html")),
    url(r'^advertise/', TemplateView.as_view(template_name="page_advertise.html")),
    url(r'^careers/', TemplateView.as_view(template_name="page_careers.html")),
    url(r'^contact-us/', TemplateView.as_view(template_name="page_contact_us.html")),
    url(r'^help/', TemplateView.as_view(template_name="page_help.html")),
    url(r'^privacy-policy/',
        TemplateView.as_view(template_name="page_privary_policy.html")),
    url(r'^team/', TemplateView.as_view(template_name="page_team.html")),
    url(r'^terms-of-use/', TemplateView.as_view(template_name="page_terms_of_use.html")),
    url(r'^signup/', TemplateView.as_view(template_name="register.html")),
    url(r'^make_user/$', views.make_user, name='make_user'),
    url(r'^select2/', include('django_select2.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    #url(r'^', include(newsletter_subscriptions_urlpatterns(backend=ModelBackend(Subscription),))),
    url(r'^media/', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ] + staticfiles_urlpatterns() + urlpatterns
