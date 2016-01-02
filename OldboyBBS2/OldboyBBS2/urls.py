"""OldboyBBS2 URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin

from bbs import  views
from  web_chat import urls as chat_urls
from web_qq import urls as web_qq_urls
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chat/', include(chat_urls)),
    url(r'^web_qq/', include(web_qq_urls)),
    url(r'^$', views.index ),
    url(r'^life/$', views.life, name='life' ),
    url(r'^tech/$', views.tech, name='tech' ),
    url(r'^1024/$', views.category1024, name='category1024' ),
    url(r'^article/(\d+)/$', views.article, name='article'),
    url(r'^article/create/$', views.create_bbs, name='create_bbs'),
    url(r'^login/$', views.account_login, name='login'),
    url(r'^latest_bbs_id/$',views.latest_bbs_id, name='get_latest_bbs_id'),


]
