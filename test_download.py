import urllib

testfile = urllib.URLopener()
try:
    testfile.retrieve("http://127.0.0.1/1.mp4", "1.mp4")
except:
    print 'error'





