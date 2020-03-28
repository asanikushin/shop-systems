#!/usr/bin/env python3

from config import BaseConfig

import smtplib
import pika
import logging
import json
import time


def send_email(address: str, message: str, subject: str = ""):
    email = "\r\n".join((
        "From: %s" % BaseConfig.FROM_EMAIL,
        "To: %s" % address,
        "Subject: %s" % subject,
        "",
        message
    ))

    server = smtplib.SMTP(BaseConfig.SMTP_URI)
    try:
        server.sendmail(BaseConfig.FROM_EMAIL, [address], email)
    except smtplib.SMTPException as smtpEx:
        logging.error(smtpEx.strerror)
    finally:
        server.quit()


def callback(ch, method, properties, body):
    logging.debug(" [x] Received %r" % (body,))
    logging.info(" [x] Received")
    data = json.loads(body)
    send_email(address=data["email"], message=data["text"], subject=data["subject"])
    logging.info(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


logging.basicConfig(
    format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("Before sleep")
time.sleep(10)
logging.info("After sleep")
logging.info(BaseConfig.QUEUE)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=BaseConfig.RABBITMQ))
channel = connection.channel()
channel.queue_declare(queue=BaseConfig.QUEUE, durable=True)

logging.info(' [*] Waiting for messages. To exit press CTRL+C')
channel.basic_consume(on_message_callback=callback, queue=BaseConfig.QUEUE)

channel.start_consuming()
