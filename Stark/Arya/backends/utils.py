#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Alex Li
import sys

from Arya import action_list
import django
django.setup()

from Stark import settings
from Arya import models
class ArgvManagement(object):
    '''
    接收用户指令并分配到相应模块
    '''
    def __init__(self,argvs):
        self.argvs = argvs
        self.argv_parse()

    def help_msg(self):
        print("Available modules:")
        for registered_module in action_list.actions:
            print("  %s" % registered_module)
        exit()
    def argv_parse(self):
        #print(self.argvs)
        if len(self.argvs) <2:
            self.help_msg()
        module_name = self.argvs[1]
        if '.' in module_name:
            mod_name,mod_method = module_name.split('.')
            module_instance  = action_list.actions.get(mod_name)
            if module_instance:#matched
                module_obj = module_instance(self.argvs,models,settings)
                module_obj.process() #提取 主机
                if hasattr(module_obj,mod_method):
                    module_method_obj = getattr(module_obj,mod_method)#解析任务，发送到队列，取任务结果
                    module_method_obj() #调用指定的指令
                else:
                    exit("module [%s] doesn't have [%s] method" % (mod_name,mod_method))
        else:
            exit("invalid module name argument")






class MsgPrint(object):

    @staticmethod
    def error(msg,exit_flag=True):
        msg = "\033[31;1mError:\033[0m%s" % msg
        print(msg)

        if exit_flag:
            exit()

