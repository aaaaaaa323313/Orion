import os
import subprocess

video_path = '/home/guanyu/Socrates/new_data_set/'
dst_path = '/home/guanyu/Socrates/data_set/'

for file in os.listdir(video_path):
    if file.endswith(".mp4"):
        f_name = video_path + file
        f_pre, _ = os.path.splitext(file)
        print f_pre

        cmd = 'ffmpeg -i ' + f_name + ' -f segment -segment_time 10 -c copy -map 0 -segment_list ' + \
                dst_path + f_pre + '.list  ' + dst_path + f_pre + '%03d.mp4'
        print cmd

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        ret = p.returncode
