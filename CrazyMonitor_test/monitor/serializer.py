#_*_coding:utf-8_*_
__author__ = 'Alex Li'

import models
import json,time
from django.core.exceptions import  ObjectDoesNotExist
class ClientHandler(object):

    def __init__(self, client_id):
        self.client_id = client_id
        self.client_configs = {
            "services":{}
        }


    def fetch_configs(self):
        try:
            host_obj = models.Host.objects.get(id=self.client_id)
            template_list= list(host_obj.templates.select_related())

            for host_group in host_obj.host_groups.select_related():
                template_list.extend( host_group.templates.select_related() )
            print(template_list)
            for template in template_list:
                #print(template.services.select_related())

                for service in template.services.select_related(): #loop each service
                    print(service)
                    self.client_configs['services'][service.name] = [service.plugin_name,service.interval]





        except ObjectDoesNotExist:
            pass

        return  self.client_configs


def get_host_triggers(host_obj):
    #host_obj = models.Host.objects.get(id=2)
    triggers = []
    for template in host_obj.templates.select_related():
        triggers.extend(template.triggers.select_related() )
    for group in host_obj.host_groups.select_related():
        for template in group.templates.select_related():
            triggers.extend(template.triggers.select_related())


    return set(triggers)

class StatusSerializer(object):
    def __init__(self,request,redis):
        self.request = request
        self.redis = redis

    def by_hosts(self):
        '''
        serialize all the hosts
        :return:
        '''
        host_obj_list = models.Host.objects.all()
        host_data_list = []
        for h in host_obj_list:
            host_data_list.append( self.single_host_info(h)  )
        return host_data_list
    def single_host_info(self,host_obj):
        '''
        serialize single host into a dic
        :param host_obj:
        :return:
        '''
        data = {
            'id': host_obj.id,
            'name':host_obj.name,
            'ip_addr':host_obj.ip_addr,
            'status': host_obj.get_status_display(),
            'last_update':None,
            'total_services':None,
            'ok_nums':None,
        }
        last_update = None
        all_service_keys = self.redis.keys("StatusData_%s*latest" % host_obj.id)
        for key in all_service_keys:
            last_data_point = self.redis.lrange(key,-1,-1)[0]
            if last_data_point:
                print('-->StatusData_%s*latest:'%key,last_data_point)

                val,save_time = json.loads(last_data_point)
                if not last_update:
                    last_update = save_time
                if save_time > last_update:
                    last_update = save_time
        data['last_update'] = time.ctime(last_update)
        data['total_services'] = len(all_service_keys)
        return  data
