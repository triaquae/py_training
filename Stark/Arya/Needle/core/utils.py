#_*_coding:utf-8_*_
__author__ = 'Alex Li'




class MsgPrint(object):

    @staticmethod
    def error(msg,exit_flag=True):
        msg = "\033[31;1mError:\033[0m%s" % msg
        print(msg)

        if exit_flag:
            exit()

