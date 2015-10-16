from django.shortcuts import render,HttpResponse

# Create your views here.
import  Queue
import  utils

msg_queue = {}

def dashboard(request):

    return  render(request,'chat/dashboard.html')



def getContactsMsgs(request):

    user_id = request.GET.get('user_id')
    if not msg_queue.has_key(user_id):
        print '--no msg queue for user :', user_id,type(user_id)
        msg_ins = msg_queue[user_id] = utils.Chat()
    msg_data = msg_queue[user_id].parse_action(request)
    print '\033[31;1m [%s] get msg  data:\033[0m' % request.user.userprofile.name ,msg_data
    return HttpResponse(msg_data)

def sendMsg(request):
    if not msg_queue.has_key('msg_recv'):
        print '----initialize pulbic msg queue...'
        msg_queue['msg_recv'] = utils.MsgParser(msg_queue)
    msg_parser = msg_queue['msg_recv'].forward_msg(request)
    return HttpResponse(msg_parser)