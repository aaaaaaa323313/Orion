import MySQLdb


if __name__ == '__main__':

    # Open database connection
    db = MySQLdb.connect("localhost","root","","test" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    try:
        cmd  = "select UNIX_TIMESTAMP(end_time) - UNIX_TIMESTAMP(start_time) from tasks;"
        cursor.execute(cmd)
        rows = cursor.fetchall()
    except:
        print 'error'

    for row in rows:
        print row

    db.close()
