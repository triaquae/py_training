#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from Weibo import settings
from app import queue_handle
from app import models
import json,os,shutil
import pika
from Weibo import settings
from app.backends import redis_conn
class WBDispathcer(object):
    '''负责接收用户所发的新微博,并进行以下操作:
    1.将此消息存入数据库
    2.检测此消息要发给哪些人
    3.检测哪些用户在线
    4.将此消息推送到所有关注发送者且在线的用户的队列里'''

    def __init__(self):
        self.q_man = queue_handle.QueueMan()
        self.redis = redis_conn.redis_conn(settings)


    def save_to_db(self,data):
        print("---存入数据库---")
        print(data)
        wb_obj = models.Weibo(
            wb_type = 0, #temp 0
            #forward_or_collect_from_id =
            user_id = data.get("user_id"),
            text= data.get("wb_text"),
            #pictures_link_id =
            #video_link_id =
            perm = 0 ,

        )
        wb_obj.save()
        self.archive_pics(data,wb_obj)
        return wb_obj
    def archive_pics(self,data,new_wb_obj):
        '''
        如果这条wb有照片,那就为其创建一个目录存放照片,目录名与表id相同
        :param data:  wb raw_data
        :param new_wb_obj: newly created wb obj in db
        :return:
        '''
        print("此条Wb包括的照片",data.get('pictures'))
        if data.get('pictures'):
            user_dir = "%s/%s" %(settings.FILE_CENTER_PATH,data.get("user_id") )
            new_wb_pic_archive_dir = "%s/%s" %(user_dir,new_wb_obj.id)
            os.mkdir(new_wb_pic_archive_dir) #
            for pic_name in data.get('pictures'):
                shutil.copyfile("%s/temp/%s" %(user_dir,pic_name),
                            "%s/%s" %(new_wb_pic_archive_dir,pic_name)  )

    def push_to_followers(self,data,db_wb_obj):
        '''
        只推送最近一天登录的关注者
        :param data:
        :return:
        '''
        print("---把新wb推给所有关注者")
        data['wb_id'] = db_wb_obj.id
        wb_user = models.UserProfile.objects.get(id=data.get("user_id"))
        print(wb_user.my_followers.select_related())

        for follower in wb_user.my_followers.select_related():
            queue_name = "uid_%s" % follower.id
            print("q_name",queue_name)
            #检测用户是否最近登录了,登录 了就给他推送

            login_recently_flag = self.redis.get("RecentLoginUser_%s" %follower.id)
            print("最近是否登录,",follower.id,login_recently_flag)

            if login_recently_flag:

                #self.q_man.channel.queue_declare(queue=queue_name,passive=True)
                self.q_man.channel.queue_declare(queue=queue_name)

                self.q_man.channel.basic_publish(exchange='',
                                      routing_key=queue_name,
                                      body=json.dumps(data) )
                print(" [x] Sent to %s " % queue_name,data)


    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)
        data = json.loads(body.decode())
        db_wb_obj = self.save_to_db(data)
        self.push_to_followers(data,db_wb_obj)

    def watch_new_wbs(self):
        '''监听所有新发的微博'''

        self.q_man.make_conn()
        self.q_man.channel.queue_declare(queue='wb_create_queue')

        self.q_man.channel.basic_consume(self.callback,
                              queue='wb_create_queue',
                              no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.q_man.channel.start_consuming()