from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.core.cache import cache
import json
from Weibo import settings
import os
from app.backends import redis_conn
# Create your views here.

REDIS_OBJ = redis_conn.redis_conn(settings)
def acc_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username=username,password=password)
        if user is not  None:
            login(request,user)
            user_dir = "%s/%s" %(settings.FILE_CENTER_PATH,request.user.userprofile.id)
            if not os.path.exists(user_dir):
                os.mkdir(user_dir)
                os.mkdir(user_dir + "/temp")
            #在redis里注册一下这个用户,并生成一个列表, 这样他关注 的人如果发了微博,就会
            print(REDIS_OBJ)
            REDIS_OBJ.set("RecentLoginUser_%s" % user.userprofile.id, True, ex=3600*12)
            return redirect("/")
        else:
           return render(request, 'app/login/login.html',{'error':'用户名密码错误!'})
    return render(request, 'app/login/login.html')


@login_required
def index(request):

    return render(request,'app/index.html')



def file_upload_test(request):
    if request.method == 'POST':
        print(request.FILES)

        file_obj = request.FILES.get('file')
        print(file_obj,dir(file_obj))
        recv_size = 0
        cache.delete(file_obj.name) #先delete原有的cache if exist
        with open('%s/%s/temp/%s' % (settings.FILE_CENTER_PATH,request.user.userprofile.id,file_obj.name), 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
                recv_size +=len(chunk)
                cache.set(file_obj.name, recv_size)

        return HttpResponse("sdddpost")
    return  render(request,'app/file_upload_test.html')



def file_upload_progress(request):
    if request.method == 'GET':
        print("----come....")
        filename = request.GET.get('filename')
        upload_progress = cache.get(filename)
        print('upload_progress:', upload_progress)

        return HttpResponse(json.dumps({"received_size":upload_progress}))
    else: #post ,clear cache key
        cache_key = request.POST.get('cache_key')
        cache.delete(cache_key)

        return HttpResponse("cache key[%s] got deleted" %cache_key)