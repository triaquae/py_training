from django.db import models

from django.contrib.auth.models import User
# Create your models here.



class BBS(models.Model):
    title = models.CharField(max_length=254,unique=True)
    category = models.ForeignKey('Category')
    author = models.ForeignKey("UserProfile")
    content = models.TextField(max_length=100000)
    breif = models.TextField(max_length=512,default='none.....')

    head_img = models.ImageField(upload_to="upload/bbs_summary/")

    publish_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    bbs = models.ForeignKey('BBS')
    parent_comment = models.ForeignKey('Comment',blank=True,null=True,related_name='p_comment')
    user = models.ForeignKey('UserProfile')
    comment = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.comment

class Thumb(models.Model):
    bbs = models.ForeignKey('BBS')
    action_choices = (('thumb_up','Thumb Up'), ('view_count',"View Count"))
    action = models.CharField(choices=action_choices,max_length=32)
    user = models.ForeignKey('UserProfile')

    def __unicode__(self):
        return "%s : %s" %(self.bbs.title,self.action)


class Category(models.Model):
    name = models.CharField(max_length=32,unique=True)
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64)
    user_groups = models.ManyToManyField('UserGroup')

    friends = models.ManyToManyField("self")
    online = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class UserGroup(models.Model):
    name = models.CharField(max_length=32,unique=True)

    def __unicode__(self):
        return self.name
