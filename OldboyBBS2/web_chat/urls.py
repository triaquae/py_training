
from django.conf.urls import include, url

import views
urlpatterns = [
    url(r'dashboard/$', views.dashboard, name='chat'),
    url(r'getContactsMsgs/$', views.getContactsMsgs, name='getContactsMsgs'),
    url(r'sendMsg/$', views.sendMsg, name='send_msg'),

]
