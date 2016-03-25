#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from django import forms
import os,time

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=255,min_length=10)
    breif = forms.CharField(max_length=255,min_length=10)
    content = forms.CharField(min_length=15)
    category_id = forms.IntegerField()
    head_img = forms.FileField()


def handle_uploaded_file(request,f):
    path = 'upload/user_uploads/%s' % request.user.userprofile.id
    if not os.path.isdir(path):
        os.mkdir(path)
    filename_with_abs = "%s/%s" %(path, f.name)
    if os.path.isfile(filename_with_abs):
        filename_with_abs += str(int(time.time()))
    with open(filename_with_abs, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename_with_abs