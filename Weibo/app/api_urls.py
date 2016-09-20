
from django.conf.urls import url
from django.contrib import admin
from  app import api_views


urlpatterns = [

    url(r'wb_creation/$', api_views.wb_create, name='wb_create'),
    url(r'get_new_wbs/(\d+)/$', api_views.get_new_wbs, name='get_new_wbs'), #只加载新wb条数
    url(r'load_new_wbs/(\d+)/$', api_views.load_new_wbs, name='load_new_wbs'),
]
