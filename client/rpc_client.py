import pika
import uuid
import json

class RPCClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, service_name, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key=service_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=json.dumps(message)
        )

        while self.response is None:
            self.connection.process_data_events()

        return self.response.decode()

# ------------- MENU PARA O USUÁRIO ---------------

rpc = RPCClient()

print("\n=== Cliente RPC ===")
print("1 - Soma")
print("2 - Média")
print("3 - Busca")
print("4 - Info do Servidor\n")

op = input("Escolha o serviço: ")

if op == "1":
    a = int(input("A: "))
    b = int(input("B: "))
    print("Resultado:", rpc.call("service_soma", {"a": a, "b": b}))

elif op == "2":
    valores = list(map(int, input("Lista (ex: 1 2 3): ").split()))
    print("Resultado:", rpc.call("service_media", {"valores": valores}))

elif op == "3":
    nome = input("Nome para buscar: ")
    print("Resultado:", rpc.call("service_busca", {"nome": nome}))

elif op == "4":
    print("Resultado:", rpc.call("service_info", {}))

else:
    print("Opção inválida!")
