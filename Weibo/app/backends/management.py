#_*_coding:utf-8_*_
__author__ = 'Alex Li'



import os,sys
import django
django.setup()
#from monitor.backends import data_processing,trigger_handler
from Weibo import settings
from app.backends import wb_dispatcher


class ManagementUtility(object):
    """
    Encapsulates the logic of the django-admin and manage.py utilities.
    A ManagementUtility has a number of commands, which can be manipulated
    by editing the self.commands dictionary.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None
        self.registered_actions = {
            'start':self.start,
            'stop': self.stop,
            'new_wb_dispatcher':self.new_wb_dispatcher,
            'user_wb_test':self.user_wb_test,

        }

        self.argv_check()

    def user_wb_test(self):
        '''测试用户wb'''
        from app import queue_handle
        q_man = queue_handle.QueueMan()
        q_man.make_conn()

        print(sys.argv)
        if len(self.argv) < 3:
            exit("must provide user id")
        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)

        user_q_name = "uid_%s"% sys.argv[2]
        q_man.channel.basic_consume(callback,
                              queue=user_q_name,
                              no_ack=True)

        print(' [%s] Waiting for messages. To exit press CTRL+C' % user_q_name)
        q_man.channel.start_consuming()

    def argv_check(self):
        '''
        do basic validation argv checks
        :return:
        '''
        if len(self.argv) < 2:
            self.main_help_text()
        if self.argv[1] not in self.registered_actions:
            self.main_help_text()
        else:
            self.registered_actions[sys.argv[1]]()
    def start(self):
        '''
        start monitor server frontend and backend
        :return:
        '''
        reactor = data_processing.DataHandler(settings)
        reactor.looping()

    def stop(self):
        '''
        stop monitor server
        :return:
        '''


    def new_wb_dispatcher(self):
        '''启动新wb处理器'''
        print("--start wb dispachter---")
        dispatcher_obj = wb_dispatcher.WBDispathcer()
        dispatcher_obj.watch_new_wbs()

    def main_help_text(self, commands_only=False):
        """
        Returns the script's main help text, as a string.
        """
        if not commands_only:
            print("supported commands as flow:")
            for k,v in self.registered_actions.items():
                print("    %s\t" % (k))
            exit()



def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
