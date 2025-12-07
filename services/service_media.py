from common.rpc_utils import get_connection, get_channel
import pika
import json

connection = get_connection()
channel = get_channel(connection)

queue_name = "service_media"
channel.queue_declare(queue=queue_name)

def media(data):
    lista = data.get("valores")
    if not lista:
        return {"error": "lista vazia ou inválida"}

    try:
        avg = sum(lista) / len(lista)
        return {"result": avg}
    except Exception as e:
        return {"error": str(e)}

def on_request(ch, method, props, body):
    try:
        data = json.loads(body.decode("utf-8"))
        response = media(data)
    except:
        response = {"error": "JSON inválido"}

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id,
            content_type="application/json"
        ),
        body=json.dumps(response)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=on_request)

print(" [x] Serviço MEDIA pronto...")
channel.start_consuming()
