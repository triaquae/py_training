from django.contrib import admin
import models

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('category','priority','title','author','publish_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','bbs','parent_comment','comment','date')
admin.site.register(models.UserProfile)
admin.site.register(models.UserGroup)
admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Category)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.Thumb)