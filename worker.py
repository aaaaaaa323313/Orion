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

    cmd = "ffmpeg -y -i " + dst_seg
    for res in tgt_res:
        tgt_seg = os.path.join(config.worker_path, seg_id + '_' + res + '.mp4')
        cmd += " -s " + res + " -strict -2 " + tgt_seg

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    ret = p.returncode
    return ret


def callback(ch, method, properties, body):
    print("Received %r" % body)
    ch.basic_ack(delivery_tag = method.delivery_tag)

    seg_id = body
    ret = download_segment(seg_id)
    if ret == -1:
        return -1

    ret = transcode(seg_id)
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

    db = MySQLdb.connect("localhost","root","lovelvyan","test" )
    cursor = db.cursor()

    connection = pika.BlockingConnection(pika.ConnectionParameters( \
            host = config.broker_server))

    channel = connection.channel()
    channel.queue_declare(queue = config.vm_name)
    channel.basic_qos(prefetch_count=1)


    channel.basic_consume(callback, queue = config.vm_name)

    channel.start_consuming()

    db.close()

