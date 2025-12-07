# service_soma.py
from common.rpc_utils import get_connection, get_channel
import pika
import json

connection = get_connection()
channel = get_channel(connection)

queue_name = "service_soma"
channel.queue_declare(queue=queue_name)

def parse_number(x):
    """Tenta converter x para int ou float; lança ValueError se inválido."""
    if isinstance(x, (int, float)):
        return x
    if isinstance(x, str):
        # tenta int primeiro, depois float
        try:
            return int(x)
        except ValueError:
            return float(x)
    raise ValueError("valor não numérico")

def soma(data):
    """
    Espera payload JSON do tipo:
    { "a": <número>, "b": <número> }
    Retorna: { "result": <soma> } ou { "error": "..."}
    """
    if not isinstance(data, dict):
        return {"error": "payload deve ser um objeto JSON"}
    if "a" not in data or "b" not in data:
        return {"error": "chaves 'a' e 'b' são obrigatórias"}
    try:
        a = parse_number(data["a"])
        b = parse_number(data["b"])
    except Exception as e:
        return {"error": f"entrada inválida: {str(e)}"}

    # mantém int se ambos forem inteiros, caso contrário float
    result = a + b
    return {"result": int(result) if isinstance(a, int) and isinstance(b, int) else result}

def on_request(ch, method, props, body):
    try:
        data = json.loads(body.decode("utf-8"))
    except Exception:
        response = {"error": "JSON inválido"}
    else:
        response = soma(data)

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

print(" [x] Serviço SOMA pronto...")
channel.start_consuming()
