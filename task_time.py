import MySQLdb


if __name__ == '__main__':

    # Open database connection
    db = MySQLdb.connect("localhost","root","lovelvyan","test" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    try:
        cmd  = "select * from tasks"
        cursor.execute(cmd)
        rows = cursor.fetchall()
    except:
        print 'error'

    for row in rows:
        print row

    db.close()
