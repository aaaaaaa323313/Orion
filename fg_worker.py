#!/usr/bin/env python
import os
import pika
import time
import urllib
import config
import MySQLdb
import subprocess
import signal
import redis
import sys

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

    cmd = "ffmpeg -y -i " + dst_seg
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


def get_pid(name):
    return subprocess.check_output(["pidof",name])

def callback(ch, method, properties, body):
   #print("Received %r" % body)

    try:
        pid = get_pid('avconv')

        pid = int(pid)
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        cur_pid = r.get('cur_pid')
        cur_sta = r.get('cur_sta')

        if pid == cur_pid and cur_sta == 1:
            os.kill(pid, signal.SIGSTOP)
            r.set('cur_sta', 0)
        elif pid == cur_pid and cur_sta == 0:
            pass
        elif pid != cur_pid:
            os.kill(pid, signal.SIGSTOP)
            r.set('cur_pid', pid)
            r.set('cur_sta', 0)
    except:
        pid = None

    ch.basic_ack(delivery_tag = method.delivery_tag)

    seg_id = body
    old_t  = time.time()
    ret = download_segment(seg_id)
    #print time.time() - old_t
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

    q = channel.queue_declare(queue = config.fg_vm_name)
    q_len = q.method.message_count
    if q_len == 0 and pid != None:
        try:
            os.kill(pid, signal.SIGCONT)
            r.set('cur_sta', 1)
        except:
            pass



if __name__ == '__main__':

    db_server = config.db_server
    db_name   = config.db_name
    db = MySQLdb.connect(db_server, "root", "", db_name)
    cursor = db.cursor()

    connection = pika.BlockingConnection(pika.ConnectionParameters( \
            host = config.broker_server))

    channel = connection.channel()
    channel.queue_declare(queue = config.fg_vm_name)
    channel.basic_qos(prefetch_count=3)


    channel.basic_consume(callback, queue = config.fg_vm_name)

    channel.start_consuming()

    db.close()

