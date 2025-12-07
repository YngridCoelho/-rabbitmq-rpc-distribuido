# 📦 Sistema de RPC Distribuído com RabbitMQ

### Projeto da disciplina de **Sistemas Distribuídos** --- Curso de **ADS / UFC**

Este projeto implementa um sistema distribuído utilizando **RabbitMQ**
como broker de mensagens e o padrão **RPC (Remote Procedure Call)** para
comunicação entre serviços.\
Ele foi desenvolvido como atividade prática da disciplina de *Sistemas
Distribuídos* do curso de **Análise e Desenvolvimento de Sistemas (ADS)
da Universidade Federal do Ceará --- UFC**.

------------------------------------------------------------------------

## 🎯 Objetivo do Projeto

O objetivo é demonstrar, de forma simples e funcional:

-   Como serviços distribuídos podem se comunicar de forma desacoplada
    usando filas de mensagens.
-   O funcionamento do padrão **RPC** aplicado a sistemas distribuídos.
-   Como implementar múltiplos serviços independentes usando
    **RabbitMQ**.
-   Como um cliente pode enviar requisições para vários serviços como se
    fossem funções locais.
-   Aplicar os conceitos teóricos da disciplina em um sistema real e
    executável.

------------------------------------------------------------------------

## 🏗 Arquitetura Geral do Projeto

A solução é composta por:

### 📁 **common/**

Módulo com funções utilitárias compartilhadas entre os serviços.

-   `rpc_utils.py` --- cria conexões e canais com RabbitMQ.

------------------------------------------------------------------------

### 📁 **services/**

Conjunto de serviços independentes, cada um com sua própria fila e
responsabilidade:

  -----------------------------------------------------------------------
  Serviço                       Fila                      Descrição
  ----------------------------- ------------------------- ---------------
  `service_soma.py`             `service_soma`            Soma dois
                                                          números.

  `service_busca.py`            `service_busca`           Busca
                                                          informações em
                                                          um banco de
                                                          dados fake.

  `service_media.py`            `service_media`           Calcula média
                                                          de uma lista de
                                                          valores.

  `service_info.py`             `service_info`            Retorna
                                                          informações do
                                                          sistema
                                                          operacional.
  -----------------------------------------------------------------------

Todos os serviços:

-   Recebem dados em formato JSON.
-   Processam a requisição.
-   Respondem via `reply_to` e `correlation_id`.

------------------------------------------------------------------------

### 📁 **client/**

Contém tudo relacionado ao cliente RPC do sistema.

  Arquivo           Função
  ----------------- --------------------------------------------
  `rpc_client.py`   Envia requisições RPC e aguarda respostas.
  `menu.py`         Interface interativa para testar serviços.

------------------------------------------------------------------------

## 🔄 Fluxo de Funcionamento

1.  O cliente envia uma requisição para a fila correspondente (ex:
    `service_soma`).
2.  O serviço retira a mensagem da fila, processa e gera uma resposta.
3.  O serviço devolve o resultado pela fila `reply_to`.
4.  O cliente recebe o retorno usando o `correlation_id`.

------------------------------------------------------------------------

## 🧰 Dependências

-   Python 3.10 ou superior\

-   RabbitMQ\

-   Biblioteca Python:

    ``` bash
    pip install pika
    ```

------------------------------------------------------------------------

## 📥 Instalação das Dependências

### 1. Instalar o RabbitMQ (Docker recomendado)

``` bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Painel Web:

    http://localhost:15672
    user: guest
    pass: guest

### 2. Instalar dependências Python

``` bash
pip install -r requirements.txt
```

Ou manualmente:

``` bash
pip install pika
```

------------------------------------------------------------------------

## ▶️ Como Executar

### 1. Certifique-se de estar na raiz do projeto

``` bash
cd rabbitmq-rpc-distribuido
```

### 2. Rodar cada serviço em um terminal separado:

``` bash
python -m services.service_soma
python -m services.service_busca
python -m services.service_media
python -m services.service_info
```

### 3. Rodar o menu interativo do cliente:

``` bash
python -m client.menu
```

------------------------------------------------------------------------

## 🧪 Exemplo de Chamadas com o Cliente

``` python
from client.rpc_client import RPCClient
rpc = RPCClient()

print(rpc.call("service_soma", {"a": 10, "b": 20}))
print(rpc.call("service_busca", {"nome": "joao"}))
print(rpc.call("service_media", {"valores": [10, 20, 30]}))
print(rpc.call("service_info", {}))
```

------------------------------------------------------------------------

## 📚 Considerações Finais

Este projeto demonstra na prática como funciona um sistema distribuído
baseado em **RPC e filas de mensagens**, permitindo modularização,
escalabilidade e baixo acoplamento entre serviços --- conceitos centrais
da disciplina de Sistemas Distribuídos da UFC.

------------------------------------------------------------------------
