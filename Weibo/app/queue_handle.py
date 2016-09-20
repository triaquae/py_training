#_*_coding:utf-8_*_
__author__ = 'Alex Li'


from  Weibo import settings
import pika
import json,time
class QueueMan(object):
    '''负责消息的发送, 接收'''
    def __init__(self):
        self.channel = None

    def make_conn(self):
        self.connection =  pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
        self.channel = self.connection.channel()

    def publish_new_wb(self,wb_data):
        '''发新wb'''
        #声明queue
        self.channel.queue_declare(queue='wb_create_queue')

        #n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
        self.channel.basic_publish(exchange='',
                              routing_key='wb_create_queue',
                              body=json.dumps(wb_data) )
        print(" [x] Sent ",wb_data)


    def on_response(self, ch, method, props, body):
        print("new wb is comming ...",ch, method, props, body)
        self.new_wb_list.append(json.loads(body.decode()))
        self.response = True

    def get_new_wbs(self,queue_name):
        '''返回此用户队列里新微博条数'''
        self.response = None
        self.new_wb_list = []
        status = self.channel.queue_declare(queue=queue_name)
        print("[%s] message count "%queue_name,status.method.message_count)

        return status.method.message_count
        # consume_obj = self.channel.basic_consume(self.on_response, no_ack=True,
        #                    queue=queue_name)
        #
        # timer = time.time()
        # while self.response is None:
        #     self.connection.process_data_events()
        #     if time.time() - timer >10:
        #         print("\033[41;1mno new msg for 10secs , break...\033[0m")
        #         self.connection._flush_output()
        #         self.connection.close()
        #         break
        # return self.new_wb_list

    def load_new_wbs(self,queue_name):
        '''
        返回此用户的新wb列表
        :param queue_name:
        :return:
        '''
        self.response = None
        self.new_wb_list = []
        status = self.channel.queue_declare(queue=queue_name)
        print("[%s] message count "%queue_name,status.method.message_count)

        consume_obj = self.channel.basic_consume(self.on_response, no_ack=True,
                           queue=queue_name)

        self.connection.process_data_events()
        print(" self.connection.process_data_events()")
        self.connection._flush_output()
        print("self.connection._flush_output()")
        self.connection.close()
        print("self.connection.close()")
        # timer = time.time()
        # while self.response is None:
        #     self.connection.process_data_events()
        #     if time.time() - timer >10:
        #         print("\033[41;1mno new msg for 10secs , break...\033[0m")
        #         self.connection._flush_output()
        #         self.connection.close()
        #         break
        return self.new_wb_list

