#!/usr/bin/env python
import os
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='vm-1')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(5)
    print 'sleep for 5 seconds'

channel.basic_consume(callback, queue='vm-1', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

