import pika
import json

params = pika.URLParameters('amqps://fuaemccq:c6tSNKTS7eXqx06Aj0HK_IuP0t-yACbA@gull.rmq.cloudamqp.com/fuaemccq')

connection = pika.BlockingConnection(params)

# create a new channel that can be published
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',routing_key='main', body=json.dumps(body), properties=properties )
    