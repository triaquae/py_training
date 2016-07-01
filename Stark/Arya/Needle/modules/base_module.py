#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from core.utils import MsgPrint

class BaseSaltModule(object):
    def __init__(self,task_obj):
        self.task_obj = task_obj


    def process(self,module_data,*args,**kwargs):

        #print('module data:',module_data,kwargs)
        print("file mod".center(60,'='))
        section_name =module_data['raw_cmds']['section']
        section_data =module_data['raw_cmds']['mod_data']
        sub_action = module_data['raw_cmds'].get('sub_action')
        print('section name:',section_name)
        for mod_item in section_data:
            for k,v in mod_item.items():
                print('\t',k,v)
                state_func = getattr(self,'func__%s'%k)
                state_func(v)

        if sub_action: #如果有,就执行,基本只针对 文件 模块
            sub_action_func = getattr(self,'func__%s' % sub_action)
            sub_action_func(module_data=module_data['raw_cmds'])

    def func__require(self,*args,**kwargs):
        print('require:',*args,**kwargs)


    def type_validate(self,item_name,data,data_type):
        if type(data) is not data_type:
            MsgPrint.error("[%s] requires %s ,not a %s" %(item_name,data_type,type(data)))