import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='vm-1')

channel.basic_publish(exchange='', routing_key='vm-1', body='guanyu')

print(" [x] Sent 'guanyu'")
connection.close()
