import pika
import json
from main import Product, db

params = pika.URLParameters('#cloud-amqp') # https://customer.cloudamqp.com/instance

connection = pika.BlockingConnection(params)

# create a new channel that can be published
channel = connection.channel()

channel.queue_declare(queue='main')

def callback(channel, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('product created')
    
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('product updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('product deleted')
    else:
        print(f"Unknown content_type occurred: {properties.content_type}")


try:
    channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
    print('Started consuming')
    channel.start_consuming()
    print('close')
    channel.close()
except Exception as exp:
    print(f'Failed to consume: {exp}')
