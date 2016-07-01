#_*_coding:utf-8_*_
__author__ = 'Alex Li'

import urllib.request
import os,shutil
from modules.base_module import BaseSaltModule

class FileModule(BaseSaltModule):


    def func__managed(self,*args,**kwargs):
        module_data = kwargs.get('module_data')
        print('\033[41;1m managed module data:\033[0m',module_data)
        target_filepath = module_data['section']
        if self.has_source:#需要把这个文件 copy 成section指定的文件
            if self.source_file is not None: #已经下载了
                shutil.copyfile(self.source_file,target_filepath)
                print('copied file from [%s] to [%s]'%(self.source_file,target_filepath) )


    def func__directory(self,*args,**kwargs):
        module_data = kwargs.get('module_data')
        print('\033[41;1m directory module data:\033[0m',module_data)

    def func__user(self,*args,**kwargs):
        pass

    def func__group(self,*args,**kwargs):
        pass


    def func__mode(self,*args,**kwargs):
        pass

    def download_http(self,file_path):
        print('donlowding from http:',file_path)
        print("downloading with urllib2")
        http_server = self.task_obj.main_obj.configs.FILE_SERVER['http']
        url_arg = "file_path=%s" % file_path
        filename= file_path.split('/')[-1]
        url = "http://%s%s?%s" % (http_server,
                                    self.task_obj.main_obj.configs.FILE_SREVER_BASE_PATH,
                                    url_arg)
        print('\033[45;1mhttpserver\033[0m ',url,self.task_obj.task_body['id'])
        f = urllib.request.urlopen(url)
        data = f.read()
        file_save_path = "%s/%s"%(self.task_obj.main_obj.configs.FILE_STORE_PATH,
                                  self.task_obj.task_body['id'])
        if not os.path.isdir(file_save_path):
            os.mkdir(file_save_path)
        with open("%s/%s" %(file_save_path,filename), "wb") as code:
            code.write(data)

        return "%s/%s" %(file_save_path,filename)
    def download_salt(self,file_path):
        print('donlowding from salt:',file_path)
    def func__source(self,*args,**kwargs):
        fileurl = args[0]
        print('downloading ...',fileurl)
        download_type,file_path = fileurl.split(":")
        file_download_func = getattr(self,'download_%s' % download_type)
        self.source_file = file_download_func(file_path)
        self.has_source = True

    def func__sources(self,*args,**kwargs):
        for file_source in args[0]:
            self.func__source(file_source)

    def func__recurse(self,*args,**kwargs):
        pass