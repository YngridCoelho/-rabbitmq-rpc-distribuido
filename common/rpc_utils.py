import pika
import os

def get_connection():
    host = os.getenv("RABBIT_HOST", "localhost")
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=host)
    )

def get_channel(connection):
    return connection.channel()
