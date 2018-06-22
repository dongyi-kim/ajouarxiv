from django.conf.urls import url, include
from django.contrib import admin

from accounts import views

urlpatterns = [
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^verify/$', views.EmailVerificationView.as_view(), name='email_verification'),
    url(r'^verify/done$', views.EmailVerificationDoneView.as_view(), name='email_verification_done'),
    url(r'^api/verification/$', views.EmailVerificationApiView.as_view(), name='api_email_verification'),
    url(r'^api/register/$', views.RegisterApiView.as_view(), name='api_register'),
    url(r'^api/login/$', views.LoginApiView.as_view(), name='api_login'),

]
