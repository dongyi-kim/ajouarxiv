from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^p/(?P<report_id>\d+)/$', views.ShortReportUrlView.as_view(), name='report_short_url'),
    url(r'^error/$', views.fail, name = 'fail'),
    url(r'^upload_ckimage/$', views.CKEditorImageUploadApiView.as_view(), name='api_image_upload_ckeditor'),
    url(r'^upload_ckfile/$', views.CKEditorFileUploadApiView.as_view(), name='api_file_upload_ckeditor')
]