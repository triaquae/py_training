#_*_coding:utf8_*_
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from  CrazyMonitor import settings
import json,time
# Create your views here.
from serializer import  ClientHandler,get_host_triggers
import json
from backends import redis_conn
from backends import data_optimization
import models
from backends import data_processing
import serializer
REDIS_OBJ = redis_conn.redis_conn(settings)

def dashboard(request):

    return render(request,'dashboard.html')

def hosts(request):
    host_list = models.Host.objects.all()
    print("hosts:",host_list)
    return render(request,'hosts.html',{'host_list':host_list})
def host_detail(request,host_id):
    host_obj = models.Host.objects.get(id=host_id)
    return render(request,'host_detail.html', {'host_obj':host_obj})
def hosts_status(request):

    hosts_data_serializer = serializer.StatusSerializer(request,REDIS_OBJ)
    hosts_data = hosts_data_serializer.by_hosts()

    return HttpResponse(json.dumps(hosts_data))
def client_configs(request,client_id):
    print("--->",client_id)
    config_obj = ClientHandler(client_id)
    config = config_obj.fetch_configs()

    if config:

        return HttpResponse(json.dumps(config))

@csrf_exempt
def service_data_report(request):
    if request.method == 'POST':
        print("---->",request.POST)
        #REDIS_OBJ.set("test_alex",'hahaha')
        try:
            print('host=%s, service=%s' %(request.POST.get('client_id'),request.POST.get('service_name') ) )
            data =  json.loads(request.POST['data'])
            #print(data)
            #StatusData_1_memory_latest
            client_id = request.POST.get('client_id')
            service_name = request.POST.get('service_name')
            data_saveing_obj = data_optimization.DataStore(client_id,service_name,data,REDIS_OBJ)

            redis_key_format = "StatusData_%s_%s_latest" %(client_id,service_name)
            #data['report_time'] = time.time()
            #REDIS_OBJ.lpush(redis_key_format,json.dumps(data))

            #在这里同时触发监控
            host_obj = models.Host.objects.get(id=client_id)
            service_triggers = get_host_triggers(host_obj)

            trigger_handler = data_processing.DataHandler(settings,connect_redis=False)
            for trigger in service_triggers:
                trigger_handler.load_service_data_and_calulating(host_obj,trigger,REDIS_OBJ)
            print("service trigger::",service_triggers)
        except IndexError as e:
            print('-->err:',e)


    return HttpResponse(json.dumps("---report success---"))
