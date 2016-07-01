from django.contrib import admin

# Register your models here.
from Arya import models
admin.site.register(models.Host)
admin.site.register(models.HostGroup)