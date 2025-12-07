import pika
import uuid
import json
import time
import os

class RPCClient:
    def __init__(self, host=None, timeout_seconds=10):
        host = host or os.getenv("RABBIT_HOST", "localhost")
        self.timeout_seconds = timeout_seconds

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.response = None
        self.corr_id = None

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def close(self):
        self.connection.close()

    def on_response(self, ch, method, props, body):
        if props.correlation_id != self.corr_id:
            return
        try:
            self.response = json.loads(body.decode("utf-8"))
        except:
            self.response = body

    def call(self, service_name, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key=service_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                content_type="application/json"
            ),
            body=json.dumps(message)
        )

        start = time.time()
        while self.response is None:
            if time.time() - start > self.timeout_seconds:
                raise TimeoutError("Timeout aguardando resposta do serviço")
            self.connection.process_data_events(time_limit=0.1)

        return self.response
