from common.rpc_utils import get_connection, get_channel
import pika
import platform
import json

connection = get_connection()
channel = get_channel(connection)

queue_name = "service_info"
channel.queue_declare(queue=queue_name)

def get_info(_):
    return {"so": platform.system(), "versao": platform.version()}

def on_request(ch, method, props, body):
    result = get_info(None)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=json.dumps(result)
    )
    ch.basic_ack(method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=on_request)

print(" [x] Serviço INFO pronto...")
channel.start_consuming()
