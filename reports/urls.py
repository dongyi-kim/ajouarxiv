from django.conf.urls import url, include
from django.contrib import admin
from ajouarxiv import settings
from django.conf.urls.static import static

from reports import views

urlpatterns = [
    url(r'^home/$', views.ReportHomeView.as_view(), name='reports_home'),
    url(r'^list/$', views.ReportListView.as_view(), name='reports_list'),
    url(r'^view/(?P<pk>\d+)/$', views.ReportDetailView.as_view(), name='reports_view'),
    url(r'^help/$', views.ReportHelpView.as_view(), name='reports_help'),
    url(r'^writings/$', views.ReportMyWritingsView.as_view(), name='reports_writings'),
    url(r'^create/$', views.ReportCreateView.as_view(), name='reports_create'),
    url(r'^modify/info/(?P<report_id>\d+)/$', views.ReportInfoModifyView.as_view(), name='reports_modify_info'),
    url(r'^modify/file/(?P<report_id>\d+)/$', views.ReportFileModifyView.as_view(), name='reports_modify_file'),
    url(r'^modify/upload/(?P<report_id>\d+)/$', views.ReportFileUploadView.as_view(), name='reports_modify_upload'),
    url(r'^download/(?P<report_id>\d+)/$', views.DownloadView.as_view(), name='reports_download'),
]
