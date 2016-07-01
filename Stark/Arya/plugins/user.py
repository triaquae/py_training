#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Alex Li
from Arya.backends.base_module import BaseSaltModule


class User(BaseSaltModule):
    def uid(self,*args,**kwargs):
        self.type_validate('uid',args[0],int)
        return "-u %s" % args[0]

    def gid(self,*args,**kwargs):
        self.type_validate('gid',args[0],int)
        return "-g %s" % args[0]
    def shell(self,*args,**kwargs):
        self.is_path('shell',args[0])
        return '-s %s'% args[0]
    def home(self,*args,**kwargs):
        self.is_path('home',args[0])
        return '-h %s'% args[0]
    def present(self,*args,**kwargs):
        print(args,kwargs)
    def fullname(self,*args,**kwargs):
        #print(args,kwargs)
        return '-c "%s"'% args[0]

    def is_required(self,*args,**kwargs):
        #print('user require',args,kwargs)
        #cmd = '''more /etc/passwd |awk -F":" '{ print $1 }'|grep "^%s$" |wc -l''' % kwargs.get('mod_val')
        cmd = r'''if [ `more /etc/passwd |awk -F":" '{ print $1 }'|grep "^%s$" |wc -l` ==  '1' ];then echo 0; else echo 1; fi;''' % kwargs.get('mod_val')
        return cmd
class UbuntuUser(User):

    def present(self,*args,**kwargs):
        username = kwargs.get('section')

        cmd_list = ["useradd"]
        single_line_arguments = ['password',]
        single_line_cmds = [] #需单独执行的命令
        #for argument in kwargs.get("mod_data"):
        for state_item in kwargs.get("mod_data"):
            for state_func_name,val in state_item.items():
                state_func = getattr(self,state_func_name)

                state_res = state_func(val,**kwargs)
                if state_res:#结果不为空
                    if state_func_name in single_line_arguments:
                        single_line_cmds.append(state_res)
                    else:
                        cmd_list.append(state_res)

        cmd_list.append(username)
        #print("sub action ",args,kwargs)
        #print('module cmd'.center(50,'-'))
        #print('cmd_list:',' '.join(cmd_list) )
        #print('single_line_cmds:',single_line_cmds)
        raw_cmds = [' '.join(cmd_list)] + single_line_cmds
        #print('raw cmds:',raw_cmds)
        #final_cmd
        return raw_cmds

    def password(self,*args,**kwargs):
        username = kwargs.get('section')
        password = args[0]
        return '''echo "%s:%s"  | sudo chpasswd''' %(username,password)