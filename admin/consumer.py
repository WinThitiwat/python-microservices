import pika
import os 
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product



params = pika.URLParameters("#cloud-amqp")

connection = pika.BlockingConnection(params)

# create a new channel that can be published
channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(channel, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print(f'Product-id:{id} likes increased!')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()
