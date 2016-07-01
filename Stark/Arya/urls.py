
from django.conf.urls import url,include


from Arya import views
urlpatterns = [

    url(r'file_center/',views.file_download),
]
