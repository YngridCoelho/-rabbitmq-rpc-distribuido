from common.rpc_utils import get_connection, get_channel
import pika
import json

connection = get_connection()
channel = get_channel(connection)

queue_name = "service_media"
channel.queue_declare(queue=queue_name)

def media(data):
    lista = data["valores"]
    return sum(lista) / len(lista)

def on_request(ch, method, props, body):
    data = json.loads(body)
    result = media(data)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=str(result)
    )
    ch.basic_ack(method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=on_request)

print(" [x] Serviço MEDIA pronto...")
channel.start_consuming()
