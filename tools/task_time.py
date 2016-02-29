import sys
import MySQLdb


if __name__ == '__main__':

    tn = sys.argv[1]
    print tn

    # Open database connection
    db = MySQLdb.connect("localhost","root","","exp_1")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    try:
        cmd  = "select UNIX_TIMESTAMP(end_time) - UNIX_TIMESTAMP(start_time) from %s where success = 1;" % tn
        cursor.execute(cmd)
        rows = cursor.fetchall()
    except:
        print 'error'

    num = 0.0
    sum = 0.0
    for row in rows:
        #print  int(row[0])
        sum += int(row[0])
        num += 1

    print sum / num
    print num

    db.close()


