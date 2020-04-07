import pika
from pika.exceptions import AMQPConnectionError

import socket
import time
import logging


def send_message(rabbit: str, queue: str, message: str):
    connection = wait_connection(rabbit, logging)
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)

    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    connection.close()


def wait_connection(host: str, logger, wait_rounds: int = 10) -> pika.BlockingConnection:
    round = 0
    cur_sleep = 1
    sum_sleep = 0
    sleep_factor = 2

    connection = None
    while round < wait_rounds:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
            break
        except (AMQPConnectionError, socket.gaierror) as ex:
            if type(ex) == socket.gaierror:
                logger.warning(f"Problems with sockets: {ex.strerror}")
            else:
                logger.warning(f"Problems with AMPQ: {ex}")
            logger.info(f"Sleep for {cur_sleep} seconds")
            time.sleep(cur_sleep)
            sum_sleep += cur_sleep
            cur_sleep *= sleep_factor
        round += 1
        connection = None
    logger.info(f"Total sleep time {sum_sleep}")
    if connection is None:
        raise TimeoutError(f"Cannot create connection with RabbitMQ {host} for {wait_rounds} rounds and "
                           f"{sum_sleep} summary waiting time")
    return connection
