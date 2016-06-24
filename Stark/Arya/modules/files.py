#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from Arya.backends.utils import MsgPrint
from Arya.modules.base_module import BaseSaltModule
from Stark import settings


class FileModule(BaseSaltModule):

    #def managed:
    def func__source(self,*args,**kwargs):
        if args[0].startswith('salt://'):
            #make sure file exist
            source_file = args[0].lstrip("salt:")
            source_path  = "%s%s" %(settings.SALT_CONFIGS,source_file)
            print(source_path)
    def func__managed(self,*args,**kwargs):
        pass
    def func__user(self,*args,**kwargs):
        self.type_validate('user',args[0],str)

    def func__group(self,*args,**kwargs):
        self.type_validate('group',args[0],str)

    def func__mode(self,*args,**kwargs):
        pass #self.type_validate('mode',args[0],str)
'''
/etc/httpd/conf/httpd.conf:
  file.managed:
    - source: salt://apache/httpd.conf
    - user: root
    - group: root
    - mode: 644
'''