from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import models
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
import  utils
import json
from django.contrib.auth import authenticate,login

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.



def account_login(request):


    if request.method == 'GET':
        return  render(request,'login.html')

    else:
        print request.POST
        username = request.POST.get('username')
        passwd = request.POST.get('password')
        user = authenticate(username=username,password=passwd)
        if user is not None:
            login(request,user)
            user.userprofile.online = True
            user.userprofile.save()
            return  HttpResponseRedirect("/")
        else:
            return  render(request,'login.html',{
                'login_err': "Wrong username or password!"
            })


def index(request):

    articles = models.BBS.objects.all().order_by('-publish_date')

    paginator = Paginator(articles, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        articles_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles_list = paginator.page(paginator.num_pages)




    return render(request,'index.html',{
        'articles': articles_list
    })

def article(request,article_id):

    try:
        article_obj = models.BBS.objects.get(id=article_id)
        #comment_tree = utils.build_comment_tree(request,article_obj)
        comment_tree = utils.create_comment_tree(request,article_obj)

        return  render(request,'article.html', {
            'article':article_obj,
            'comment_tree':comment_tree
        })
    except  ObjectDoesNotExist:
        raise  Http404("Article you looking for is not exist!")

def latest_bbs_id(request):
    return  HttpResponse(
       models.BBS.objects.latest('publish_date').id
    )

def create_bbs(request):

    if request.method == 'GET':

        return  render(request,'create_bbs.html')
        #return render_to_response()
    elif request.method == 'POST':
        print request.POST,request.FILES

        #obj = models.BBS.objects.create() no return
        obj = models.BBS(
            title = request.POST.get('title'),
            content = request.POST.get('content'),
            category_id = 1,
            author_id = 1,

        )

        obj.save()

        #save file
        filename = utils.handle_upload_file(request,request.FILES["head_image"])
        obj.head_img = 'upload/%s' %filename
        obj.save()
        print obj.id

        return render(request,'create_bbs.html',{
            'new_article': obj
        })

def life(request):

    return  render(request,'life.html')

def tech(request):

    return  render(request,'tech.html')
def category1024(request):

    return  render(request,'1024.html')