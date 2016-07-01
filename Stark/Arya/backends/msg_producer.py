#_*_coding:utf-8_*_
__author__ = 'Alex Li'


import pika,pickle
from Stark import settings


class MsgProducer(object):
    def __init__(self,view_obj):
        self.view_obj = view_obj
        self.make_connection()
    def make_connection(self):
        self.mq_conn = pika.BlockingConnection(pika.ConnectionParameters(
                       settings.MQ_CONN['host']))
        self.mq_channel = self.mq_conn.channel()

    def publish(self,data):
        print('\033[41;1m-----going to publish msg ------\033[0m',data)

        task_data = {
            'callback_queue': 'TASK_CALLBACK_%s' % 1,
            'data':data

        }

        print('--', self.view_obj.hosts)

        for host in self.view_obj.hosts:
            #声明queue
            queue_name = 'TASK_Q_%s' %host.id
            self.mq_channel.queue_declare(queue=queue_name)


            #n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
            self.mq_channel.basic_publish(exchange='',
                                  routing_key=queue_name,
                                  body= pickle.dumps(task_data))
            print(" [x] Sent task to queue [%s] 'Hello World!'" % queue_name)

        self.mq_conn.close()

    def callback(self):
        '''
        get task callback
        :return:
        '''
        pass