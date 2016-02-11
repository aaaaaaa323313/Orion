import os

video_path = '/home/guanyu/Socrates/new_data_set/'
dst_path = '/home/guanyu/Socrates/data_set/'

for file in os.listdir(video_path):
    if file.endswith(".mp4"):
        f_name = video_path + file
        f_pre, _ = os.path.splitext(file)
        print f_pre

        #cmd = 'ffmpeg -i ' + f_name + ' -f segment -segment_time 10 -c copy -map 0 -segment_list ' + \
        #    50mb.list 50mb%03d.mp4

