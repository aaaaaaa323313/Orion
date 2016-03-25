#!/usr/bin/env python
import os
import pika
import time
import urllib
import config
import MySQLdb
import subprocess


db = None
cursor = None
worker_path = config.worker_path
global channel

def download_segment(seg_id):
    seg = urllib.URLopener()
    try:
        url = "http://127.0.0.1/" + seg_id + '.mp4'
        dst_seg = os.path.join(config.worker_path, seg_id + '.mp4')
        seg.retrieve(url, dst_seg)
        return 0
    except:
        return -1

def transcode(seg_id):
    tgt_res = config.target_resolution
    dst_seg = os.path.join(config.worker_path, seg_id + '.mp4')

    cmd = "avconv -y -i " + dst_seg
    for res in tgt_res:
        tgt_seg = os.path.join(config.worker_path, seg_id + '_' + res + '.mp4')
        cmd += " -c:v libx264 -c:a aac " + " -s " + res + " -strict -2 " + tgt_seg

    #print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    ret = p.returncode
    if ret != 0:
        print ret
    return ret


def callback(ch, method, properties, body):
    #q = channel.queue_declare(queue = config.bg_vm_name)
    #q_len = q.method.message_count
    #print q_len
    #print("Received %r" % body)
    ch.basic_ack(delivery_tag = method.delivery_tag)

    seg_id = body
    old_t  = time.time()
    ret = download_segment(seg_id)
    #print time.time() - old_t
    if ret == -1:
        return -1

    ret = transcode(seg_id)
    #print ch.method.message_count
    if ret == 0:
        cmd = "UPDATE tasks SET end_time = now(), success = 1  WHERE \
                segment_id = \"%s\"" % seg_id

        try:
            cursor.execute(cmd)
            db.commit()
        except:
            db.rollback()
            print 'db error'



if __name__ == '__main__':

    db_server = config.db_server
    db_name   = config.db_name
    db = MySQLdb.connect(db_server, "root", "", db_name)
    cursor = db.cursor()

    connection = pika.BlockingConnection(pika.ConnectionParameters( \
            host = config.broker_server))

    channel = connection.channel()
    channel.queue_declare(queue = config.bg_vm_name)
    channel.basic_qos(prefetch_count=3)


    channel.basic_consume(callback, queue = config.bg_vm_name)

    channel.start_consuming()

    db.close()

