#_*_coding:utf-8_*_
__author__ = 'Alex Li'


from Arya.backends.utils import MsgPrint
from Arya.modules.base_module import BaseSaltModule

class UserModule(BaseSaltModule):


    def func__present(self,*args,**kwargs):
        print('present')
        username,uid= None,None
        for item in self.module_data:
            if item.get('username'):
                username = item.get('username')
                break
            if item.get('uid'):
                uid = item.get('uid')
                break
        #if username :
        #    cmd = '''cat /etc/passwd|awk -F":" '{print $1}' |grep '^%s$' ''' %username
        #elif uid:
        #    cmd = '''cat /etc/passwd|awk -F":" '{print $3}' |grep '^%s$' ''' %uid
        if username or uid:
            return True
        else:
            MsgPrint.error("neither argument [username] or [uid] exist in user module section")
        #complete_cmd = '''
        #    get_user_id=%s`
        #    if [ ${#get_user_id} > 0 ];then
        #       echo "bigger than 0"
        #    else
        #       echo 'small'
        #    fi
        #'''%cmd

        #return complete_cmd
    def func__uid(self,*args,**kwargs):
        #print('uid ....',*args,**kwargs)
        #print(self.module_data)
        self.type_validate('uid',args[0],int)
        #for item in self.module_data:
        #    if item.get('home'):
                #user_home = item['home']
                #cmd = 'chown -R %s %s ' %(args[0],user_home)
                #print('to cmd:',cmd)
                #return cmd
    def func__gid(self,*args,**kwargs):
        #print('gid ....',*args,**kwargs)
        self.type_validate('gid',args[0],int)
    def func__home(self,*args,**kwargs):
        #print('home ....',*args,**kwargs)
        self.type_validate('home',args[0],str)
        #return True
    def func__shell(self,*args,**kwargs):
        #print('shell ....',*args,**kwargs)
        self.type_validate('shell',args[0],str)
        #return True
    def func__username(self,*args,**kwargs):
        #return self.func__present(*args,**kwargs)
        #return True
        self.type_validate('shell',args[0],str)