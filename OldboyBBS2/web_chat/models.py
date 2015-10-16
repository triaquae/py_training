from django.db import models

# Create your models here.
from bbs import models as bbs



class QQGroup(models.Model):
    name = models.CharField(max_length=64)
    founder = models.ForeignKey(bbs.UserProfile)
    members = models.ManyToManyField(bbs.UserProfile,blank=True,related_name='group_members')
    admins = models.ManyToManyField(bbs.UserProfile,blank=True,related_name='group_admins')
    member_limit = models.IntegerField(default=200)
    def __unicode__(self):
        return  self.name
