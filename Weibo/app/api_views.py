from django.shortcuts import render,HttpResponse

# Create your views here.

import json,time
from app import queue_handle
import logging

#logging.basicConfig(level=logging.DEBUG)

#程序启动先建立与rabbitmq的连接,以后就不用重复建立了
# queue_man = queue_handle.QueueMan()
# queue_man.make_conn()

def response_formatter(response_type,response_code,data):
    response_types ={
        0:'success',
        1:'error',
        2: 'warning'
    }
    if response_type == 1: #error

        formatted_data = {
            'status':response_types[response_type],
            'code' : response_code,
            'error': data
        }
    else:
        formatted_data = {
            'status':response_types[response_type],
            'code' : response_code,
            'data': data
        }

    return formatted_data


def wb_create(request):

    print(request.POST.get("data"))

    #把新wb发到消息队列
    wb_data = json.loads(request.POST.get("data"))
    wb_data['timestamp'] = time.time()
    queue_man = queue_handle.QueueMan()
    queue_man.make_conn()
    queue_man.publish_new_wb(wb_data)

    response = response_formatter(0,200,wb_data)


    return HttpResponse(json.dumps(response))


def get_new_wbs(request,user_id):
    '''用户定时检测有没有新微博,返回 新wb条数'''

    # q_man = queue_handle.QueueMan()
    # q_man.make_conn()
    # q_man.get_new_wbs("uid_%s" % user_id)
    queue_man = queue_handle.QueueMan()
    queue_man.make_conn()
    new_wb_count = queue_man.get_new_wbs("uid_%s" % user_id)
    print("-----gew new wb---done",new_wb_count)
    return HttpResponse(json.dumps({'new_wb_count':new_wb_count}))


def load_new_wbs(request,user_id):

    queue_man = queue_handle.QueueMan()
    queue_man.make_conn()
    new_wb_list = queue_man.load_new_wbs("uid_%s" % user_id)
    return HttpResponse( json.dumps({'new_wb_list':new_wb_list}))