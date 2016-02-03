import pika
import time
import config
import string
import random
import MySQLdb


def id_gen(size=6, chars = string.ascii_uppercase + string.digits + \
        string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def declare_queue(channel):
    for i in range(1, config.max_vm_num + 1):
        vm_name = 'vm_' + str(i)
        channel.queue_declare(queue = vm_name)
    return 0




if __name__ == '__main__':

    connection = pika.BlockingConnection(pika.ConnectionParameters( \
                host='localhost'))
    channel = connection.channel()

    declare_queue(channel)

    # Open database connection
    db = MySQLdb.connect("localhost","root","lovelvyan","test" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    i = 0;

    while True:
        i = i + 1;
        seg_id = id_gen()
        try:
            cmd = "INSERT INTO tasks VALUES (0, \"%s\", %d, NULL, NULL)" % (seg_id, 1)
            #print cmd
            cursor.execute(cmd)
            db.commit()

        except:
            db.rollback()
            print 'error'

        vm_name = 'vm_' + str(i%10 +1)

        channel.basic_publish(exchange='', routing_key = vm_name, body = seg_id)
        print(" [x] Sent " + seg_id)



   #db.close()
   #connection.close()



