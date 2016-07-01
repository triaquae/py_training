#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Alex Li
from Arya.backends.base_module import BaseSaltModule


class File(BaseSaltModule):



    def managed(self,*args,**kwargs):
        #print('\033[33;1mmanaged.m\033[0m',args,kwargs)
        kwargs['sub_action'] = 'managed'
        self.data['file_source'] = True
        return kwargs
    def user(self,*args,**kwargs):
        pass
    def group(self,*args,**kwargs):
        pass
    def mode(self,*args,**kwargs):
        pass
    def is_required(self,*args,**kwargs):
        #print('file  require',args,kwargs)
        cmd = r'''ls %s; echo $?'''  % kwargs.get('mod_val')
        return cmd
    def directory(self,*args,**kwargs):
        kwargs['sub_action'] = 'directory'
        return self.managed(*args,**kwargs)
    def source(self,*args,**kwargs):
        #print('source:',args,kwargs)
        return [args[0]]
    def sources(self,*args,**kwargs):
        #print('sources:',args,kwargs)
        return args[0]
    def recurse(self,*args,**kwargs):
        pass