import shlex
import subprocess

cmd = '/usr/bin/avconv -y -i 50mb.mp4 -s 426x240 -strict experimental test.mp4'
p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
stdout, stderr = p.communicate()
ret = p.returncode
print p.pid
