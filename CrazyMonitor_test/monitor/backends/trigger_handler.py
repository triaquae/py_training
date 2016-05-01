#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from monitor.backends import redis_conn
import pickle
class TriggerHandler(object):

    def __init__(self,django_settings):
        self.django_settings = django_settings
        self.redis = redis_conn.redis_conn(self.django_settings)



    def start_watching(self):
        '''
        start listening and watching the needed to be handled triggers from other process
        :return:
        '''

        radio = self.redis.pubsub()
        radio.subscribe(self.django_settings.TRIGGER_CHAN)
        radio.parse_response() #ready to watch
        print("\033[43;1m************start listening new triggers**********\033[0m")
        self.trigger_count = 0
        while True:
            msg = radio.parse_response()
            self.trigger_consume(msg)


    def trigger_consume(self,msg):
        self.trigger_count +=1
        print("\033[41;1m************Got a trigger msg [%s]**********\033[0m" % self.trigger_count)
        trigger_msg = pickle.loads(msg[2])
        #print("msg:",pickle.loads(msg[2]))
        print(trigger_msg)
        print(trigger_msg['positive_expressions'][0]['expression_obj'])
