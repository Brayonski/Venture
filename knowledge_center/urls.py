from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import include, url
from knowledge_center import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),
        name='knowledge_center_home'),
    url(r'^document-reports/$', views.HomeView.as_view(),
        name='knowledge_center_document_home'),
    url(r'^read-content/(?P<pk>\d+)/$',
        views.TextMediaView.as_view(), name='knowledge_center_read_content'),
    url(r'^read-content/filter/(?P<pk>\d+)/$',
        views.TextFilterView.as_view(), name='knowledge_center_read_content_filter'),
    url(r'^read-content/sub-filter/(?P<pk>\d+)/$',
        views.SubCategoryTextFilterView.as_view(), name='knowledge_center_sub_content_filter'),
    url(r'^video-content/filter/(?P<pk>\d+)/$',
        views.VideoFilterView.as_view(), name='knowledge_center_video_content_filter'),
    url(r'^video-content/(?P<pk>\d+)/$',
        views.SingleVideoContentView.as_view(), name='knowledge_center_video_content'),
    url(r'^videos/$', views.VideoContentView.as_view(),
        name='knowledge_center_video_home'),
]
