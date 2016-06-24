#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from Stark.action_list import actions

class HouseManager(object):
    '''
    整个stark家族套件的任务分配入口
    '''

    def __init__(self,argvs):
        self.argvs = argvs[1:]

    def execute_from_command_line(self):

        self.argv_parse_and_invoke()

    def handle_sys_args(self,args,action):

        #print(args,action)
        url_matched_flag = False
        if len(args) == 0:
            if len(action[0].strip())  == 0:
                #print('matched...',action[1])
                url_matched_flag =True
        elif args[0] == action[0].strip() or args[0].split('.')[0] == action[0]:
            url_matched_flag = True
            #print('matched..dd',action[1])
        if url_matched_flag == True:
            return True

    def argv_parse_and_invoke(self):
        #print(self.argvs)
        for action in actions:
            #print(action)
            #if len(self.argvs) == 0 :#no follow args
            #    print(action)
            if self.handle_sys_args(self.argvs,action):#matched this url
                if type(action[1]) is list: #has sub layer urls
                    #print("has sub layer...")
                    for sub_action in action[1]:
                        if self.handle_sys_args(self.argvs[1:],sub_action): #matched sub action
                            if hasattr(sub_action[1],'__call__'):
                                print('sub action', sub_action[1])
                                self.commands = action
                                obj = sub_action[1](self)
                                obj.call()
                            break
                elif hasattr(action[1],'__call__'):
                    #print(type(action[1]))
                    self.commands = action
                    action[1](self)

                break
        else:
            print('invalid command')