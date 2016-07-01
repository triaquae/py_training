#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Alex Li

from  Arya.backends.utils import MsgPrint
import os

class BaseSaltModule(object):
    def __init__(self,sys_argvs,db_models,settings,**kwargs):
        self.db_models = db_models
        self.settings = settings
        self.sys_argvs = sys_argvs
        self.kwargs = kwargs
        self.data = { #最后解析生成的data就存在这里
            'raw_cmds':None,
            'pre_requisite':None,
            'watch_list':None
        }

    def get_selected_os_types(self):
        data = {}
        for host in self.host_list:
            data[host.os_type] = []
        #print('--->data',data)
        return data
    def process(self):
        self.fetch_hosts()
        self.config_data_dic = self.get_selected_os_types()

    def require(self,*args,**kwargs):
        #print('\033[41;1mrequired\033[0m'.center(50,'-'))
        os_type = self.kwargs.get('os_type')
        required_check_cmd_list = []
        for require_item in args[0]:
            #print('require:',require_item)
            for base_mod_name in require_item:
                mod_instance = self.get_module_instance(base_mod_name,os_type)
                mod_obj = mod_instance(self.sys_argvs,self.db_models,self.settings,os_type=os_type)
                #下面的cmd_res 返回的是一条命令,用于检测依赖的组件是否存在
                cmd_res = mod_obj.is_required(mod_name=base_mod_name,mod_val=require_item[base_mod_name])
                if cmd_res:
                    required_check_cmd_list.append(cmd_res)
                else:
                    MsgPrint.error("require item %s didn't return a valid result"%require_item)
        #print('--required check cmds:', required_check_cmd_list)
        self.data['pre_requisite'] = required_check_cmd_list
        #return required_check_cmd_list
        #print('\033[41;1mend required\033[0m'.center(50,'-'))



    def fetch_hosts(self):
        print('--fetching hosts---')

        if '-h' in self.sys_argvs or '-g' in self.sys_argvs:
            host_list = []
            if '-h' in self.sys_argvs:
                host_str_index = self.sys_argvs.index('-h') +1
                if len(self.sys_argvs) <= host_str_index:
                    exit("host argument must be provided after -h")
                else: #get the host str
                    host_str = self.sys_argvs[host_str_index]
                    host_str_list = host_str.split(',')
                    host_list += self.db_models.Host.objects.filter(hostname__in=host_str_list)
            if '-g' in self.sys_argvs:
                group_str_index = self.sys_argvs.index('-g') +1
                if len(self.sys_argvs) <= group_str_index:
                    exit("group argument must be provided after -g")
                else: #get the group str
                    group_str = self.sys_argvs[group_str_index]
                    group_str_list = group_str.split(',')
                    group_list = self.db_models.HostGroup.objects.filter(name__in=group_str_list)
                    for group in group_list:
                        host_list += group.hosts.select_related()
            self.host_list = set(host_list)
            if not self.host_list: #不能为空
                MsgPrint.error("cannot find any matched host")
            #return True
            print('----host list:', host_list)
        else:
            exit("host [-h] or group[-g] argument must be provided")


    def syntax_parser(self,section_name,mod_name,mod_data):
        #print("-going to parser state data:",section_name,mod_name)
        for state_item in mod_data:
            print("\t",state_item)
            for key,val in state_item.items():
                if hasattr(self,key):
                    state_func = getattr(self,key)
                    state_func(val,secion=section_name,mod_data=mod_data)
                else:
                    MsgPrint.error("module [%s] has no argument [%s]" %( mod_name,key ))
        else: #最后处理mod subaction
            sub_action_name = mod_name.split('.')[1]
            sub_action_func = getattr(self,sub_action_name)
            self.data['raw_cmds'] = sub_action_func(section=section_name,mod_data=mod_data)
            #mod_data.append({mod_name.split('.')[1]:True}) #add sub action into mod_data for later processing
            #print("final parse result of [%s]:"% mod_name, self.data)
            return self.data
    def is_path(self,item_name,data):
        if not data:
            MsgPrint.error("[%s] argument must be a path,cannot be none" %(item_name)   )
        elif  '/' not in data:
            MsgPrint.error("[%s] argument must be a path" %(item_name)   )

    def type_validate(self,item_name,data,data_type):
        if type(data) is not data_type:
            print(data,type(data))
            MsgPrint.error("[%s] requires %s ,not a %s" %(item_name,data_type,type(data)))

    def get_module_instance(self,base_mod_name,os_type):
        plugin_file_path = "%s/%s.py" % (self.settings.SALT_PLUGINS_DIR,base_mod_name)
        if os.path.isfile(plugin_file_path):
            #导入 模块
            module_plugin = __import__('plugins.%s' %base_mod_name)
            special_os_module_name = "%s%s" %(os_type.capitalize(),base_mod_name.capitalize())
            module_file= getattr(module_plugin, base_mod_name) # 这里才是真正导入模块
            if hasattr(module_file, special_os_module_name): #判断有没有根据操作系统的类型进行特殊解析 的类，在这个文件里
                module_instance = getattr(module_file, special_os_module_name)
            else:
                module_instance = getattr(module_file, base_mod_name.capitalize())
            return module_instance
            #开始调用 此module 进行配置解析
        else:
            MsgPrint.error("module [%s] is not exist" % base_mod_name)


    def is_required(self,*args,**kwargs):
        mod_name = kwargs.get('mod_name')
        mod_val = kwargs.get('mod_val')
        print("mod_name[%s]  mod_val[%s]" % (mod_name,mod_val))
        MsgPrint.error("module [%s] cannot be invoked as 'require' argument from other module" % mod_name)