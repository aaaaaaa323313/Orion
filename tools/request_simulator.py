import os
import math
import time
import random
import pickle
import pika
import glob
import config
import string
import MySQLdb
import shutil
from random import choice


def id_gen(size=6, chars = string.ascii_uppercase + string.digits + \
        string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def declare_queue(channel):
    for i in range(1, config.max_vm_num + 1):
        vm_name = 'vm_' + str(i)
        channel.queue_declare(queue = vm_name)
    return 0

def copy_video_seg(seg_id):
    segs = glob.glob("/home/guanyu/Socrates/data_set/*.mp4")
    src_seg = random.choice(segs)
    dst_seg = os.path.join(config.content_path, seg_id + '.mp4')
    shutil.copyfile(src_seg, dst_seg)
    return 0


if __name__ == '__main__':

    connection = pika.BlockingConnection(pika.ConnectionParameters( \
                host='localhost'))
    channel = connection.channel()

    declare_queue(channel)

    # Open database connection
    db = MySQLdb.connect("localhost","root","","exp_1")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    f = open('arrive_time.pkl', 'r')
    arrive_time = pickle.load(f)

    duration = 60 * 60 * 10
    start_time = time.time()

    while True:
        cur_time = time.time()
        if cur_time - start_time > duration:
            break

        if len(arrive_time) == 0:
            break

        x = arrive_time[0]
        if x < cur_time - start_time:
            x = arrive_time.pop(0)
            print x, ' ', cur_time - start_time

            #submit_task
            seg_id = id_gen()
            copy_video_seg(seg_id)

            #vm_name = 'vm_' + str(i%10 +1)
            vm_name = 'vm_' + str(8)

            try:
                cmd = "INSERT INTO tasks VALUES (NULL, \"%s\", \"%s\", NULL, 0, 0)" % (seg_id, vm_name)
                cursor.execute(cmd)
                db.commit()
            except:
                db.rollback()
                print 'error'

            channel.basic_publish(exchange='', routing_key = vm_name, body = seg_id)
            print("Sent: " + seg_id)

        else:
            time.sleep(0.1)


    db.close()
    connection.close()




