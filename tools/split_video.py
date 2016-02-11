import os

video_path = '/home/guanyu/Socrates/new_data_set/'

for file in os.listdir(video_path):
    if file.endswith(".mp4"):
        print(file)
