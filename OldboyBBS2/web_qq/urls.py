
from django.conf.urls import include, url

import views
urlpatterns = [
    url(r'^$', views.dashboard, name='web_qq_dashboard'),
    url(r'^send_msg/$',views.send_msg,name="qq_send_msg"),
    url(r'^get_msg/$',views.get_msg,name="qq_get_msg"),



]
