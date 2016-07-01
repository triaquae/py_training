from django.db import models

# Create your models here.

class Host(models.Model):
    hostname = models.CharField(max_length=128,unique=True)
    key = models.TextField()
    status_choices = ((0,'Waiting Approval'),
                      (1,'Accepted'),
                      (2,'Rejected'))


    os_type_choices =(
        ('redhat','Redhat\CentOS'),
        ('ubuntu','Ubuntu'),
        ('suse','Suse'),
        ('windows','Windows'),
    )

    os_type = models.CharField(choices=os_type_choices,max_length=64,default='redhat')
    status = models.SmallIntegerField(choices=status_choices,default=0)

    def __str__(self):
        return self.hostname
class HostGroup(models.Model):
    name =  models.CharField(max_length=64,unique=True)
    hosts = models.ManyToManyField(Host,blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):

    datetime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id