import pika

def get_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )

def get_channel(connection):
    return connection.channel()
