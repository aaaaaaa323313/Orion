import json
import time
import urllib2


f = open('trace.dat','w')

while True:
    #try:
        content = urllib2.urlopen("https://api.twitch.tv/kraken/streams/summary").read()
        x = json.loads(content)
        res = str(time.time()) + '      ' + str(x['channels']) + '\n'
        f.write(res)
        f.flush()
        time.sleep(60)

   # except:
        print 'error'
        #continue

f.close()
