#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Alex Li
from Arya.backends.base_module import BaseSaltModule


class Pkg(BaseSaltModule):

    pass



class UbuntuPkg(Pkg):

    def installed(self,*args,**kwargs):
        #print('pkg installed:',args,kwargs)
        #cmd_list = ["sudo apt-get install -y --force-yes"]
        cmd_list = ["apt-get install -y --force-yes"]
        single_line_arguments =[]
        single_line_cmds = []
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
        return raw_cmds
    def is_required(self,*args,**kwargs):
        #print('pkg require got called...',args,kwargs)
        pkg_name = kwargs.get("mod_val")
        #cmd = "apt-get install %s |echo $?" % pkg_name
        cmd = "sudo apt-get install %s |echo $?" % pkg_name
        return cmd
    def pkgs(self,*args,**kwargs):
        #print('\033[43;1mpkgs:\033[0m',args,kwargs)

        packages = []
        for p in args[0]:
            if type(p) is dict:#has version provided
                for p_item in p:
                    packages.append("%s=%s" % (p_item,p[p_item]) )
            else:
                packages.append(p)
        return ' '.join(packages)
        #print('pkg pachakges',packages)