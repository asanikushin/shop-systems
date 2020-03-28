import pika


def send_message(rabbit: str, queue: str, message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)

    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    connection.close()
