
from django.conf.urls import url, include
from django.contrib import admin

from community import views

urlpatterns = [
    url(r'^council/$', views.StudentCouncilListView.as_view(), name='community_council'),
    url(r'^club/$', views.StudyClubListView.as_view(), name='community_club'),
    url(r'^gallery/$', views.GalleryView.as_view(), name='community_gallery'),
    url(r'^notice/$', views.NoticeListView.as_view(), name='community_notice'),
    url(r'^notice/write/$', views.NoticeCreateView.as_view(), name='community_notice_write'),
    url(r'^notice/view/(?P<pk>\d+)/$', views.NoticeView.as_view(), name='community_notice_view'),
    url(r'^notice/modify/(?P<pk>\d+)/$', views.NoticeUpdateView.as_view(), name='community_notice_modify'),

    url(r'^post/$', views.PostListView.as_view(), name='community_post'),
    url(r'^post/write/$', views.PostCreateView.as_view(), name='community_post_write'),
    url(r'^post/view/(?P<pk>\d+)/$', views.PostView.as_view(), name='community_post_view'),
    url(r'^post/modify/(?P<pk>\d+)/$', views.PostUpdateView.as_view(), name='community_post_modify'),
]
