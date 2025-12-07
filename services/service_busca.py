from common.rpc_utils import get_connection, get_channel
import pika
import json
import time

connection = get_connection()
channel = get_channel(connection)

queue_name = "service_busca"
channel.queue_declare(queue=queue_name)

FAKE_DB = {
    "joao": {"idade": 22, "cidade": "São Paulo"},
    "ana": {"idade": 30, "cidade": "Curitiba"},
    "mario": {"idade": 28, "cidade": "Recife"}
}

def busca(data):
    time.sleep(1)
    nome = data["nome"].lower()
    return FAKE_DB.get(nome, "não encontrado")

def on_request(ch, method, props, body):
    data = json.loads(body)
    result = busca(data)

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

print(" [x] Serviço BUSCA pronto...")
channel.start_consuming()
