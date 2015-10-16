from django.contrib import admin

import  models
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ('parent_comment','comment')
    list_filter = ('parent_comment','comment')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name','online')

admin.site.register(models.BBS)
admin.site.register(models.Category)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.Thumb)
admin.site.register(models.UserProfile,UserProfileAdmin)
admin.site.register(models.UserGroup)