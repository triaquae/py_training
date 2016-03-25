from django.shortcuts import render,HttpResponse
import models
from django.core.exceptions import ObjectDoesNotExist
from forms import ArticleForm,handle_uploaded_file
# Create your views here.



def index(request):
    '''
    home page
    :param request:
    :return:
    '''
    bbs_list = models.Article.objects.all()
    return  render(request,'index.html',
                   {'bbs_list':bbs_list})


def article_detail(request,article_id):

    try:
        article_obj = models.Article.objects.get(id=article_id)
    except ObjectDoesNotExist as e:
        return render(request,'404.html', {'err_msg':"Article is not exist!"})

    return render(request,'article.html', {'article_obj':article_obj})

def new_article(request):
    categorys = models.Category.objects.all()
    if request.method == 'POST':
        print(request.POST)
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            print("form is valid")
            print(request.FILES)
            data = form.cleaned_data
            del data['head_img']
            uploaded_filename = handle_uploaded_file(request,request.FILES['head_img'])
            data['author_id'] = request.user.userprofile.id
            try:
                new_article_obj = models.Article(**data)
                new_article_obj.head_img = uploaded_filename
                new_article_obj.save()
            except Exception as e:
                return HttpResponse(e)
            return render(request,'create_article.html',{'new_article_obj':new_article_obj})
        else:
            print(form.errors)
            return render(request,'create_article.html', {'categorys':categorys,
                                                          'form':form})
    return render(request,'create_article.html', {'categorys':categorys})