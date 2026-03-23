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


def conectar():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        print(f"[Cliente] Conectado ao servidor {HOST}:{PORT}")

        nome = input("[Cliente] Digite seu nome: ")
        cliente.sendall(nome.encode("utf-8"))
        
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