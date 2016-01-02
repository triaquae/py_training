from django.shortcuts import render,HttpResponse

# Create your views here.
import  utils
import json,datetime
import models
from django.core.exceptions import ObjectDoesNotExist
global_msg_dic = {
}

def dashboard(request):

    return  render(request,'web_qq/dashboard.html')



def send_msg(request):

    print request.POST
    print request.GET

    msg_data = request.POST.get('data')
    if msg_data:
        msg_data = json.loads(msg_data)
        print '-->',msg_data
        if msg_data.get('contact_type') == 'single':
            msg_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not global_msg_dic.has_key(msg_data['to_id']):
                global_msg_dic[msg_data['to_id']] =utils.ChatHandle()
            global_msg_dic[msg_data['to_id']].queue.put(msg_data)
            print "\033[32;1mpush %s into user [%s]'s queue\033[0m" %(msg_data,msg_data['to_id'])
        elif msg_data.get('contact_type') == 'group':
            group_id = msg_data['contact_id']
            group_obj = models.ChatGroup.objects.get(id=group_id)

            for u in group_obj.members.select_related():#loop all the users in this group
                if not global_msg_dic.has_key(u.id):
                    global_msg_dic[u.id] =utils.ChatHandle()
                global_msg_dic[u.id].queue.put(msg_data)
                print "\033[31;1mpush group msg %s into user [%s]'s queue\033[0m" %(msg_data,u.id)

    return HttpResponse("msg send success")

def get_msg(request):
    uid = request.GET.get('uid')
    new_msgs =[]
    if uid:
        try:
            print global_msg_dic
            user_obj = models.bbs.UserProfile.objects.get(id=uid)
            if not global_msg_dic.has_key(str(user_obj.id)):
                global_msg_dic[str(user_obj.id)] = utils.ChatHandle()
            new_msgs = global_msg_dic[str(user_obj.id)].get_msg(request)
        except ObjectDoesNotExist,e:
            print '\033[41;1m%s\033[0m' % str(e)

    return HttpResponse(json.dumps(new_msgs))