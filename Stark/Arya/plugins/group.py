#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Alex Li
from Arya.backends.base_module import BaseSaltModule


class Group(BaseSaltModule):

    def gid(self,*args,**kwargs):
        self.type_validate('gid',args[0],int)
        return '-g %s'%args[0]

    def present(self,*args,**kwargs):
        groupname = kwargs.get('section')

        cmd_list = ["groupadd %s" %groupname]
        single_line_arguments = ['addusers',]
        single_line_cmds = [] #需单独执行的命令
        for state_item in kwargs.get("mod_data"):
            for state_func_name,val in state_item.items():
                state_func = getattr(self,state_func_name)

                state_res = state_func(val,**kwargs)
                if state_res:#结果不为空
                    if state_func_name in single_line_arguments:
                        single_line_cmds.append(state_res)
                    else:
                        cmd_list.append(state_res)

        raw_cmds = [' '.join(cmd_list)] + single_line_cmds
        #print('raw cmds:',raw_cmds)
        #final_cmd
        return raw_cmds
    def is_required(self,*args,**kwargs):
        cmd = r'''if [ `more /etc/group |awk -F":" '{ print $1 }'|grep "^%s$" |wc -l` ==  '1' ];then echo 0; else echo 1; fi;''' % kwargs.get('mod_val')
        return cmd