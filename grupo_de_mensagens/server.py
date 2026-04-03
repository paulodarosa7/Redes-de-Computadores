import threading
from time import sleep
from datetime import datetime
import socket


HOST = "0.0.0.0"
PORT = 9003

WAITING_TIME = 3


# Fila de mensagens
FILA = []
pessoas = {}

# # Semáforo de acesso à fila
SEMAFORO_ACESSO = threading.Semaphore(1) # Apenas 1 thread pode acessar a fila por vez

# Quantidade de itens. Quem insere na fila, incrementa. Quem consome, decrementa.
SEMAFORO_ITENS = threading.Semaphore(0)  # A fila inicia com 0 elementos



def produzir(mensagem):
    global FILA
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Inclui a mensagem na fila
    FILA.append(mensagem)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Informa que há itens na fila.
    SEMAFORO_ITENS.release() 

def consumir():
    global FILA
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda até que existam itens na fila
    SEMAFORO_ITENS.acquire()

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Verifica se há mensagens na fila
    if FILA:
        # Retira a primeira mensagem da fila
        mensagem = FILA.pop(0)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Retorna a mensagem que estava na fila
    return mensagem

# def thread_produtora(id_thread, mensagem_cliente):
#     # Inclui mensagens na fila
#     id_msg = 0
    
#     while True:
#         msg_produzida = f"{mensagem_cliente}"
#         print(f"[Thread {id_thread} recebeu] {msg_produzida}", flush=True)
#         produzir(msg_produzida)
#         id_msg += 1
#         sleep(1)

# def thread_consumidora(id_thread):
#     # Retira mensagens da fila
#     while True:
#         msg_consumida = consumir()
#         print(f"[Thread {id_thread} consumiu] {msg_consumida}", flush=True)
#         sleep(1)


def atender_cliente(conn, addr, clientes):
    nome = clientes["nome"]
    addr = clientes["IP"]
    conn = clientes["conn"]
    
    hora_mensagem = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[Server]{nome}:{addr} - Entrou no grupo.", flush=True) 

    with conn:
        while True:
            #trabalho com as mensagens enviadas da outra ponta
            data = conn.recv(1024)
            clientes["mensagem"] = data.decode("utf-8")
            
            #guardo também a mensagem no dict, se não fizer isso envia mensagem de outro cliente
            mensagem = clientes["mensagem"]
            # print(clientes)
            # confirma que recebeu
            print(f"[Server]  Produzindo mensagem de {addr}: {mensagem}...", flush=True )
            
            
            resposta = (f">{nome}[{addr}] : {hora_mensagem} ]\n- {mensagem}")
            recebeMensagem(resposta)  # Insere a mensagem do cliente na fila
            print(f"[Cliente] {nome} enviou mensagem ao grupo.", flush=True)
            # for cliente in pessoas.values():
            #     if cliente == conn:
            #         print(f"[Server] enviando mensagem para {cliente['nome']}", flush=True)
            #         enviaMensagem()
            # conn.sendall("mensagem enviada para o grupo".encode("utf-8"))
            for cliente in pessoas.values():
                print(f"[Server] Respondido para {cliente['nome']}", flush=True)
            
    print(f"[Server] Conexão encerrada {addr}", flush=True)


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            # nome = input(f"Digite o nome do cliente {nome}: ".encode("utf-8")) # Solicita o nome do cliente 
            nome = conn.recv(1024).decode("utf-8") # recebe o nome do cliente
            # atribui o nome do cara ao endereço ip no dicionário
            pessoas[addr] = {
                "nome": nome,
                "IP": addr,
                "conn": conn,
                "mensagem": "",
                }
            #inicia a thread
            thread = threading.Thread(
                target=atender_cliente,
                args=(conn, addr, pessoas[addr]),
                daemon=True
            )
            thread.start()


def recebeMensagem(mensagem_cliente): #tread produtora  
    # Inclui mensagens na fila
    id_msg = 0
    print("[LOG] Produtor de mensagens inciado.", flush=True  )
    msg_produzida = f"{mensagem_cliente}"
    print(f"[Server] recebendo mensagem: '({msg_produzida})'", flush=True)
    produzir(msg_produzida)
    id_msg += 1
    sleep(1)

def enviaMensagem(): #thread consumidora
    while True:
        print(f"[LOG] Consumidor de mensagens inciado.", flush=True)
        msg_enviada = consumir() # Retira a mensagem da fila,
        for cliente in pessoas.values():
            print(f"[Server] mensagem enviada: {msg_enviada}", flush=True)
            conn = cliente["conn"]
            conn.sendall(f"\n{msg_enviada}".encode("utf-8"))
            print(f"[Server] Mensagens enviadas para {cliente['nome']}", flush=True)
            # sleep(WAITING_TIME)
            
            
# if __name__ == "__main__":
#     iniciar_servidor()



def main():

    # Cria a thread produtora
    t0 = threading.Thread(
                target=recebeMensagem, args=(0,), # Será a thread 0
                daemon=True
            )

    # Cria 2 threads consumidoras
    t1 = threading.Thread(
                target=enviaMensagem, # Será a thread 1
                daemon=True
            )
    t2 = threading.Thread(
                target=enviaMensagem, # Será a thread 2
                daemon=True
            )
    
    # t0.start()
    t1.start()
    t2.start()
    
    iniciar_servidor()

    
    # t0.join()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
    