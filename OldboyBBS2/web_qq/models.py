from django.db import models

# Create your models here.

from bbs import  models as bbs
class ChatGroup(models.Model):
    name = models.CharField(max_length=64)
    brief = models.CharField(max_length=254,default="nothing here....")
    founder = models.ForeignKey(bbs.UserProfile)
    members = models.ManyToManyField(bbs.UserProfile,blank=True,related_name='chat_group_members')
    admins = models.ManyToManyField(bbs.UserProfile,blank=True,related_name='chat_group_admins')
    member_limit = models.IntegerField(default=200)
    def __unicode__(self):
        return  self.name
