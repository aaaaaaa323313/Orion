#!/usr/bin/python

import os
import sys
import time
import random
import subprocess
from converter import Converter

basepath = '/home/guanyu/Socrates/data_set/'
new_path = '/home/guanyu/Socrates/new_data_set/'
c = Converter()


for fname in os.listdir(basepath):
    path = os.path.join(basepath, fname)
    if os.path.isdir(path):
        continue

    _, ext = os.path.splitext(path)
    if ext == '.mp4':
        info = c.probe(path)

        if info.video.video_width == 1280:
            #print info.video.video_width, 'x', info.video.video_height
            dur = info.format.duration
            #print dur/60.0

        if dur > 3*60 and dur < 10*60:
            os.rename(path, new_path + fname)
            print dur/60.0
        #print info.video.video_width, 'x', info.video.video_height
        #print info.video.video_fps
        #print info.video.bitrate
        #print info.video.codec


