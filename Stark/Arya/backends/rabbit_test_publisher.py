#_*_coding:utf-8_*_
__author__ = 'Alex Li'

import pika
from Stark import settings
connection = pika.BlockingConnection(
                pika.ConnectionParameters(settings.MQ_CONN['host']))
channel = connection.channel()

#声明queue
channel.queue_declare(queue='hello')


#n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()