# coding: utf-8
"""sharbrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from sharbrary.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^sharing/', include('sharing.urls')),
	url(r'^library/', include('library.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^change_lang/', TemplateView.as_view(template_name='base/lang_change.html'), name="lang_change"),
    url(r'^howto/', TemplateView.as_view(template_name='base/howto.html'), name="how_to"),
)

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
