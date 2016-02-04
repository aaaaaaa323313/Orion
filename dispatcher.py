import os
import pika
import time
import glob
import config
import string
import random
import MySQLdb
import shutil


def id_gen(size=6, chars = string.ascii_uppercase + string.digits + \
        string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def declare_queue(channel):
    for i in range(1, config.max_vm_num + 1):
        vm_name = 'vm_' + str(i)
        channel.queue_declare(queue = vm_name)
    return 0

def copy_video_seg(seg_id):
    segs = glob.glob("/var/www/video_lib/*.mp4")
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
    db = MySQLdb.connect("localhost","root","lovelvyan","test" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    i = 0;
    while i < 1000:
        i = i + 1;
        seg_id = id_gen()
        copy_video_seg(seg_id)
        vm_name = 'vm_' + str(i%10 +1)

        try:
            cmd = "INSERT INTO tasks VALUES (NULL, \"%s\", \"%s\", NULL, 0, 0)" % (seg_id, vm_name)
            cursor.execute(cmd)
            db.commit()
        except:
            db.rollback()
            print 'error'

        channel.basic_publish(exchange='', routing_key = vm_name, body = seg_id)
        print("Sent: " + seg_id)

    db.close()
    connection.close()



