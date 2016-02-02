#!/usr/bin/python
import time
import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","lovelvyan","test" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

start_time = time.time()
cur_time = 0

while cur_time - start_time < 60:
    try:
        cmd = "INSERT INTO tasks VALUES (0, \"%s\", %d, %d, %d)" % ('abcd', 1, 0, 0)
        #print cmd
        cursor.execute(cmd)
        db.commit()

    except:
        db.rollback()
        print 'error'

    cur_time = time.time()

# disconnect from server
db.close()



