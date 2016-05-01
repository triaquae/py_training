

from django.conf.urls import url

import views

urlpatterns = [

    url(r'^$',views.dashboard ),
    url(r'hosts/$',views.hosts ,name='hosts'),
    url(r'hosts/(\d+)/$',views.host_detail ,name='host_detail'),
    #url(r'client/service/report/$',views.service_data_report )

]
