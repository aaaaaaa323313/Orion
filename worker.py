#!/usr/bin/env python
import os
import pika
import time
import config





def callback(ch, method, properties, body):
    print("Received %r" % body)



if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters( \
            host = config.broker_server))

    channel = connection.channel()
    channel.queue_declare(queue = config.vm_name)

    channel.basic_consume(callback, queue = config.vm_name, no_ack = True)

    channel.start_consuming()

