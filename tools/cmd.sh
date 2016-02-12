ffmpeg -i 50mb.mp4 -f segment -segment_time 10 -c copy -map 0 -segment_list 50mb.list 50mb%03d.mp4


