#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from conf import configs,registered_modules
import pika
import pickle,threading
class CommandManagement(object):
    def __init__(self,argvs):
        self.argvs = argvs[1:]
        self.argv_handler()

    def argv_handler(self):
        if len(self.argvs) == 0:
            exit("argument: start\stop")
        if hasattr(self,self.argvs[0]):
            func = getattr(self,self.argvs[0])
            func()
        else:
            exit("invalid argument.")

    def start(self):
        client_obj = Needle()
        client_obj.listen()

    def stop(self):
        pass

class TaskHandle(object):
    def __init__(self,main_obj,task_body):
        self.main_obj = main_obj
        self.task_body = pickle.loads(task_body)

    def processing(self):
        '''
        process task
        :return:
        '''
        self.syntax_parser()
    def syntax_parser(self):
        print('----parse task ----')
        for section_name,mod_data in self.task_body['data'].items():
            print('\033[32;1msection:\033[0m',section_name)
            for mod_name,state_data in mod_data.items():
                print('  ',mod_name)
                if '.' in mod_name:
                    module_name,state_name = mod_name.split('.')
                    state_data.append({state_name:True})

                for state_item in state_data:
                    print('\t',state_item)


class Needle(object):

    def __init__(self):
        self.make_connection()
        self.client_id = self.get_needle_id()
        self.task_queue_name = "TASK_Q_%s" % self.client_id

    def get_needle_id(self):
        '''
        去服务器端取自己的id
        :return:
        '''
        return configs.NEEDLE_CLIENT_ID
    def listen(self):
        '''
        开始监听服务器的call
        :return:
        '''
        self.msg_consume()
    def make_connection(self):
        self.mq_conn = pika.BlockingConnection(pika.ConnectionParameters(
                       configs.MQ_CONN['host']))
        self.mq_channel = self.mq_conn.channel()

    def publish(self,data):
        print('\033[41;1m-----going to publish msg ------\033[0m',data)

        #声明queue
        self.mq_channel.queue_declare(queue='hello')
        #n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
        self.mq_channel.basic_publish(exchange='',
                              routing_key='hello',
                              body='Hello World!')
        print(" [x] Sent 'Hello World!'")
        self.mq_conn.close()

    def msg_callback(self,ch, method, properties, body):
            print(" [x] Received a task msg " )
            thread = threading.Thread(target=self.start_thread,args=(body,))
            thread.start()
    def start_thread(self,task_body):
        print('\033[31;1m start a thread to process task\033[0m')
        task = TaskHandle(self,task_body)
        task.processing()
    def msg_consume(self):

        self.mq_channel.queue_declare(queue=self.task_queue_name)

        #def callback(ch, method, properties, body):
        #    print(" [x] Received %r" % body)

        self.mq_channel.basic_consume(self.msg_callback,
                              queue=self.task_queue_name,
                              no_ack=True)

        print(' [%s] Waiting for messages. To exit press CTRL+C' % self.task_queue_name)
        self.mq_channel.start_consuming()