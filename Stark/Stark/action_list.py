#_*_coding:utf-8_*_
__author__ = 'Alex Li'


from Arya import command_list
from Stark import views


actions = [
    ('',views.help, ),
    ('salt', command_list.actions,'Arya salt'),
]