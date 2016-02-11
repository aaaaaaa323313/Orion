#!/usr/bin/python

import os
import sys
import time
import random
import subprocess
from converter import Converter


tgt_res = ['854x480', '640x360', '426x240']
basepath = '/home/guanyu/Socrates/data_set/'
c = Converter()

f = open('trans_res.dat','w')


for fname in os.listdir(basepath):
    path = os.path.join(basepath, fname)
    if os.path.isdir(path):
        continue

    name, ext = os.path.splitext(path)
    if ext == '.mp4':

        cmd = "ffmpeg -y -i " +  path
        for res in tgt_res:
            tgt_seg = name + '_' + res + '.mp4'
            cmd += " -s " + res + " -strict -2 " + tgt_seg

        print cmd

        start_time = time.time()
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        ret = p.returncode
        if ret != 0:
            continue

        elapsed_time = time.time() - start_time
        res = str(elapsed_time) + '\n'
        print res,
        f.write(res)
        f.flush()


f.close()


