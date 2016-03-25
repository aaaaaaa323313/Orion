import subprocess
import psutil
import signal
import redis
import time
import os
import sys

def get_pid(name):
    return subprocess.check_output(["pidof",name])


try:
    pid = get_pid('avconv')
except subprocess.CalledProcessError:
    print 'no process detected'
    sys.exit()

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

time.sleep(3);
os.kill(pid, signal.SIGCONT)
r.set('cur_sta', 1)

