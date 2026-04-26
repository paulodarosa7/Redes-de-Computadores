import socket
import threading



HOST = "127.0.0.1"
PORT = 9002


def receber_mensagem(serv):
    while True:
        try:
            dados = serv.recv(1024)
            
            if not dados:
                print("[Cliente] Conexão fechada pelo servidor.")
                break
            
            resposta = dados.decode("utf-8")
            print(f"[Server] {resposta}")
        except:
            print("[Cliente] Conexão perdida com o servidor.")
            break

# def enviar_mensagem(cliente):
#     cep = input("[Cliente] Digite o CEP: ")
#     cliente.sendall(cep.encode("utf-8"))
#     nome = input("[Cliente] Digite o nome: ")
#     cliente.sendall(nome.encode("utf-8"))
#     fruta = input("[Cliente] Digite a fruta: ")
#     cliente.sendall(fruta.encode("utf-8"))
#     mse = input("[Cliente] Minha sogra é?: ")
#     cliente.sendall(mse.encode("utf-8"))

def conectar():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:

        cliente.connect((HOST, PORT))
        print(f"[Cliente] Conectado ao servidor {HOST}:{PORT}")

        nome = input("[Cliente] Digite seu nome: ")
        cliente.sendall(nome.encode("utf-8"))
        
        dados = cliente.recv(1024)
    
        NOME = input()
        cliente.sendall(NOME.encode("utf-8"))
        FRUTA = input()
        cliente.sendall(FRUTA.encode("utf-8"))
        CEP = input()
        cliente.sendall(CEP.encode("utf-8"))
        MSE = input()
        cliente.sendall(MSE.encode("utf-8"))

        
        
        thread = threading.Thread(
            target=receber_mensagem,
            args=(cliente,)
        )
        thread.start()
        thread.join()


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
#     cliente.connect((HOST, PORT))
#     print(f"[Cliente] Conectado ao servidor {HOST}:{PORT}")
    
#     while True:
#             thread = threading.Thread(
#                 target=atender_cliente,
#                 args=(conn, addr),
#                 daemon=True
#             )
#             thread.start()
    
#     cliente.sendall(mensagem.encode("utf-8"))

#     resposta = cliente.recv(1024).decode("utf-8")
#     print(f"[Server] {resposta}")


if __name__ == "__main__":
    conectar()