from django.db import models

# Create your models here.



class HostGroup(models.Model):
    name = models.CharField(max_length=64,unique=True)
    hosts = models.ManyToManyField('Host',blank=True)

    def __str__(self):
        return self.name

class Host(models.Model):
    hostname = models.CharField(max_length=128,unique=True)

    auth_key = models.TextField(blank=True,null=True)
    status_choices =((0,'Need approval'),(1,'Accepted'))
    status = models.SmallIntegerField(choices=status_choices,default=0)
    def __str__(self):
        return self.hostname