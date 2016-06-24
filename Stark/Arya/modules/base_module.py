#_*_coding:utf-8_*_
__author__ = 'Alex Li'


from Arya.backends.utils import MsgPrint


class BaseSaltModule(object):
    def __init__(self,view_obj):
        self.view_obj = view_obj
        '''self.module_parse_dic = { #save module parse result
            'cmd':[],
            'require':None,
            'watch':None,
            'scp' :None
        }'''


    def process(self,module_data,*args,**kwargs):

        print('module data:',module_data,kwargs.get('state_mod'))
        '''if hasattr(self,state_function):
            func = getattr(self,state_function)
            res = func(*args,**kwargs)
            return res
        else:
            exit("state module has no function [%s]" % state_function)

        '''
        self.module_data = module_data
        state_mod = kwargs.get('state_mod') #may be user.present
        if state_mod:
            if '.' in state_mod: #means this mod name must be format like "user.present"
                state_func_name = state_mod.split('.')[1]
                module_data.append({state_func_name:[]}) #put this state func item into module_data,so below code will handle it
        for state_item in module_data:
            #print('------->',state_item)
            for key,val in state_item.items():
                state_function_name = 'func__%s' % key
                #print(state_function_name)
                if hasattr(self,state_function_name):
                    state_func = getattr(self,state_function_name)
                    func_to_cmd = state_func(val)
                    #print('state_function_name to cmd:',func_to_cmd)
                else:
                    MsgPrint.error("cannot find state function [%s] configured in your yaml file" % key)

    def func__require(self,*args,**kwargs):
        print('require:',*args,**kwargs)


    def type_validate(self,item_name,data,data_type):
        if type(data) is not data_type:
            MsgPrint.error("[%s] requires %s ,not a %s" %(item_name,data_type,type(data)))