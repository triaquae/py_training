#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from Arya.backends.template import templates
from Stark import settings
import os,sys
from Arya import module_list as salt_modules
from  Arya.backends import utils
from  Arya.backends import msg_producer
import django
django.setup()
from Arya import models

class ViewBase(object):
    def __init__(self,command_handler_obj):
        self.command_handler_obj = command_handler_obj

        self.host_match_str = self.fetch_hosts()

    def fetch_hosts(self):
        print('fetching hosts....')
        print(self.command_handler_obj.argvs)
        hosts = []
        if '-h' in self.command_handler_obj.argvs or '-g' in self.command_handler_obj.argvs:

            if '-h' in self.command_handler_obj.argvs:
                host_str_index = self.command_handler_obj.argvs.index('-h') +1
                if len(self.command_handler_obj.argvs) > host_str_index:
                    host_str_list = self.command_handler_obj.argvs[host_str_index].split(',')
                    for host_str in host_str_list:
                        hosts += models.Host.objects.filter(hostname__contains=host_str)
                else:
                    exit('lack of host argument after -h')

            if '-g' in self.command_handler_obj.argvs:
                group_str_index = self.command_handler_obj.argvs.index('-g') +1
                if len(self.command_handler_obj.argvs) > group_str_index:
                     group_str_list = self.command_handler_obj.argvs[group_str_index].split(',')
                     for group_str in group_str_list:
                         group_list = models.HostGroup.objects.filter(name__contains=group_str)
                         for group_obj in group_list:
                            hosts += group_obj.hosts.select_related()

                else:
                    exit('lack of host argument after -g')
            hosts = set(hosts)
            if hosts:
                self.hosts = hosts
            else:
                utils.MsgPrint.error("cannot find any matched host")
        else:
            exit('must with host [-h] or group [-g] argument provided')

    def call(self):
        print('run calling....')
        try:
            self.module_name,self.sub_action = self.command_handler_obj.argvs[1].split('.')
            if hasattr(self,self.sub_action):
                sub_func = getattr(self,self.sub_action)
                sub_func()
            else:
                exit("can not find sub action [%s] in module [%s]" %(self.sub_action,self.module_name))
        except (IndexError,ValueError) as e:
            exit('lack of sub action of this module[%s]'%self.command_handler_obj.argvs[1] )


    def load_state_files(self,state_filename):

        from yaml import load, dump
        try:
            from yaml import CLoader as Loader, CDumper as Dumper
        except ImportError:
            from yaml import Loader, Dumper

        state_file_path = "%s/%s" %(settings.SALT_CONFIGS,state_filename)
        if os.path.isfile(state_file_path):
            with open(state_file_path) as f:
                data = load(f.read(), Loader=Loader)
                return data
        else:
            utils.MsgPrint.error("%s is not a valid yaml config file" % state_filename)
class state(ViewBase):
    '''
    manage and apply state files
    '''

    def apply(self):
        '''
        load and apply state file
        :return:
        '''
        print('apply ....',self.command_handler_obj.argvs)
        if '-f' in self.command_handler_obj.argvs:
            yaml_file_index = self.command_handler_obj.argvs.index('-f') +1
            if len(self.command_handler_obj.argvs) > yaml_file_index:
                yaml_filename = self.command_handler_obj.argvs[yaml_file_index]
                print(settings.SALT_CONFIGS)
                state_data = self.load_state_files(yaml_filename)
                self.syntax_parser(state_data) #配置文件合法性验证
                #接下来直接发布任务
                task_obj = msg_producer.MsgProducer(self)
                task_obj.publish(state_data)

            else:
                utils.MsgPrint.error("lack yaml file specified after -f")
        else:
            utils.MsgPrint.error("lack yaml file specified")

    def syntax_parser(self,data):
        '''
        parse state syntax
        :param data: state data
        :return:
        '''
        for section_name,section in data.items():
            print('section:',section_name)
            for state_mod,mod_data in section.items():
                state_mod_name = state_mod.split('.')[0]
                print('\t%s' %state_mod)
                #print('\t\t',mod_data)
                if state_mod_name in salt_modules.registered_modules:
                    print('--',state_mod_name)
                    module_obj = salt_modules.registered_modules[state_mod_name](self)
                    module_obj.process(mod_data,state_mod=state_mod)
        #上面那些都是在做配置文件合法性验证,如果走到这没退出,那就代表 没什么问题
        return True




def help(obj):
    commands = obj.commands
    if len(commands)>2:
        module_name = commands[2]
        print("\033[31;1m[%s]\033[0m"% module_name)
        for action_name in commands[1]:
            print('\t%s'%action_name[0])

    else:
        utils.MsgPrint.error("action [%s] lack of moudle name argument" %commands[0])

