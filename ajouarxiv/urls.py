"""ajouarxiv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from ajouarxiv import settings
import webserver.views
from django.conf.urls.static import static

from django.views.generic import TemplateView
from django.conf.urls import (
    handler404
)

handler404 = 'webserver.views.handler404'

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  # for auth
                  url(r'^accounts/', include('accounts.urls')),
                  # url(r'^accounts/', include('django.contrib.auth.urls')),
                  url(r'^reports/', include('reports.urls')),
                  url(r'^community/', include('community.urls')),
                  url(r'', include('webserver.urls')),
				  url(r'^.well-known/pki-validation/4C2FAE1FB1B9C69A57023114C8A589B3.txt$', TemplateView.as_view(template_name="4C2FAE1FB1B9C69A57023114C8A589B3.txt", content_type="text/plain"), name="pki-validation-file"),
				  url(r'^.well-known/pki-validation/BE96CE659AFDF56CB3E16724765E4E41.txt$', TemplateView.as_view(template_name="BE96CE659AFDF56CB3E16724765E4E41.txt", content_type="text/plain"), name="pki-validation-file"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
