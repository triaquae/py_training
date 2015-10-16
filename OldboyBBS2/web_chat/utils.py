#_*_coding:utf-8_*_
__author__ = 'jieli'

import  Queue
import json,datetime
import  models
from bbs import models as bbs_models

class Chat(object):

    def __init__(self):

        #self.request = request
        self.msg_q = Queue.Queue()
        #self.init = True # after the first get from web page , this flag will set to false, use this to determine whether need to hold the request for 60s or not


    def parse_action(self,request):
        self.request = request
        action = request.GET.get("action")
        func = getattr(self,action)

        res = func()

        return res

    def update_info(self): #get latest contact list and msgs
        data = {
            'contact_dic': self.get_contacts(),
            'msg_list': self.get_msg()
        }
        #print data
        return json.dumps(data)

    def get_contacts(self):
        user_obj = bbs_models.UserProfile.objects.get(id=self.request.user.userprofile.id)
        contacts =user_obj.friends.select_related().values('id','name','online')
        groups = user_obj.group_members.select_related().values('id','name')
        #print 'contacts of %s:' % self.request.user.userprofile.name, contacts
        contact_dic ={
            'contacts': list(contacts),
            'groups': list(groups)
        }

        return  contact_dic

    def get_msg(self):
        test_msg = {
            'contact_type': 'single_contact', # 'group'
            'contact_id' : 1, # talk to some one
            'from':{'id':1,'name':'Alex'},
            'msg': "Test msg haha!!",
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        msg_list = []
        print 'queue msgs of user %s' % self.request.user.userprofile.id ,self.msg_q.qsize()

        for i in range(self.msg_q.qsize()):
            msg = self.msg_q.get()
            msg_list.append(msg)
        if self.msg_q.qsize() == 0:
            try:
                init_flag = self.request.GET.get('init')
                print '--init flag', init_flag
                if init_flag is None:
                    print '**********no new msg for user[%s]****waiting******' % self.request.user.userprofile.name
                    new_msg = self.msg_q.get(timeout=60) #hold request for 60 secs at most
                    msg_list.append(new_msg)
                else:
                    print '******[%s] first time pull contact info, no block*****'  % self.request.user.userprofile.name
            except Queue.Empty,e:
                print '\033[41;0mNo new msg for user[%s],exit\033[0m' % self.request.user.userprofile.name
        return  msg_list


class MsgParser(object):

    def __init__(self,msg_queue):
        self.all_msg_queues = msg_queue
        #self.pulbic_q = Queue.Queue() #no need this

    def forward_msg(self,request):
        print '-->going to parse msg:', request.GET

        callback= {'err':[],'msg':[]}

        msg_dic = request.GET.get('data')
        if msg_dic:
            msg_dic = json.loads(msg_dic)
            contact_id = msg_dic['to'] #msg forward to who
            msg_dic['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg_dic['to'] = contact_id
            contact_type = msg_dic['contact_type']
            if contact_type == 'single_contact':
                user_obj = models.bbs.UserProfile.objects.get(id=int(contact_id))
                if not self.all_msg_queues.has_key(contact_id):#user not login yet , create a msg queue for this user # here might will be a mem killer in the future

                    self.all_msg_queues[contact_id] = Chat()
                    print "--not find user %s's msg q,create one " % user_obj.name,type(contact_id)
                try:
                    self.all_msg_queues[contact_id].msg_q.put_nowait(msg_dic)  #push msg to this user's msg queue
                    print("pushed data into user %s's msg queue" % user_obj.name)
                except Queue.Full,e:
                    callback['err'].append("contact %s 's msg box is full"  % user_obj.name)
            elif contact_type == 'group':
                group_obj = models.QQGroup.objects.get(id=int(contact_id))
                for member in group_obj.members.values():
                    if not request.user.userprofile.id == member['id']: #don't send to the user self  whom sent this msg again.
                        if not self.all_msg_queues.has_key(str(member['id'])):#user not login yet , create a msg queue for this user # here might will be a mem killer in the future
                            self.all_msg_queues[str(member['id'])] = Chat()
                            print "--not find user %s's msg q,create one " % member['name'],type(contact_id)
                        try:
                            self.all_msg_queues[str(member['id'])].msg_q.put_nowait(msg_dic)  #push msg to this user's msg queue
                            print("pushed data into user %s's group [%s] msg queue" % (member['name'],group_obj.name))
                        except Queue.Full,e:
                            callback['err'].append("contact %s 's msg box is full"  % member['name'])

        print '\033[32;1mforwared msg:\033[0m',msg_dic, callback
        return 'msg forwarded'