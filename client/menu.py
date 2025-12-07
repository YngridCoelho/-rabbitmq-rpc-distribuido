from client.rpc_client import RPCClient

def menu():
    rpc = RPCClient()

    while True:
        print("\n=== MENU RPC DISTRIBUÍDO ===")
        print("1 - SOMA (service_soma)")
        print("2 - BUSCA (service_busca)")
        print("3 - MÉDIA (service_media)")
        print("4 - INFO DO SISTEMA (service_info)")
        print("0 - SAIR")
        opc = input("\nEscolha uma opção: ")

        # --------------------------------------------------
        # 0 - sair
        if opc == "0":
            print("Encerrando...")
            rpc.close()
            break

        # --------------------------------------------------
        # 1 - SOMA
        elif opc == "1":
            try:
                a = float(input("Digite o valor de A: "))
                b = float(input("Digite o valor de B: "))
                resp = rpc.call("service_soma", {"a": a, "b": b})
                print("\n>> Resultado:", resp)
            except:
                print("Entrada inválida!")

        # --------------------------------------------------
        # 2 - BUSCA
        elif opc == "2":
            nome = input("Nome para buscar (joao, ana, mario): ")
            resp = rpc.call("service_busca", {"nome": nome})
            print("\n>> Resposta:", resp)

        # --------------------------------------------------
        # 3 - MÉDIA
        elif opc == "3":
            lista_str = input("Digite valores separados por vírgula: ")
            try:
                valores = [float(x.strip()) for x in lista_str.split(",")]
                resp = rpc.call("service_media", {"valores": valores})
                print("\n>> Média:", resp)
            except:
                print("Formato inválido!")

        # --------------------------------------------------
        # 4 - INFO
        elif opc == "4":
            resp = rpc.call("service_info", {})
            print("\n>> Informações do sistema:", resp)

        # --------------------------------------------------
        else:
            print("\nOpção inválida!")


if __name__ == "__main__":
    menu()
