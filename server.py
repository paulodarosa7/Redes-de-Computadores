import socket
import threading
import random
import string
from time import sleep

HOST = "0.0.0.0"
PORT = 9002

WAITING_TIME = 3

respostas = {
    "CEP": "",
    "NOME": "",
    "FRUTA": "",
    "MSÉ": ""
}


letra_sorteada = random.choice(string.ascii_letters)

stop = threading.Event()
jogadores = {}
def atender_cliente(conn, addr):

    n_data = conn.recv(1024)
    nome = n_data.decode("utf-8")
    jogadores[addr] = nome

    conn.sendall(f"{nome} seja bem-vindo ao meu servidor! \n".encode("utf-8"))

    print(f"[Server] Nova conexão {addr}", flush=True)

    respostas = {
        "CEP": "",
        "NOME": "",
        "FRUTA": "",
        "MSÉ": ""
    }
    conn.sendall(b"Vamos jogar stop! \n")
    
    if len(jogadores) < 2:
        conn.sendall(b"Esperando mais jogadores...\n")
    else:
        conn.sendall(b"Jogador encontrado!\nIniciando jogo...\n")
        sleep(WAITING_TIME)
        conn.sendall("A letra sorteada eh: {}".format(letra_sorteada.lower()).encode("utf-8"))
        conn.sendall(f"\nResponda com uma palavra que comece com a letra sorteada. >>> {letra_sorteada.lower()} <<<\n".encode("utf-8"))

        with conn:
            while not stop.is_set():
                conn.sendall(b"JOGO INICIADO!!!!!!!")
                data = conn.recv(1024)
                mensagem = data.decode("utf-8")
                print(f"[Server] Recebido de {addr}: {mensagem}", flush=True )
                print(f"[Server] Processando respostas..", flush=True )
                sleep (WAITING_TIME)
                resposta = mensagem.lower()
                respostas["CEP"] = resposta
                respostas["NOME"] = resposta
                respostas["FRUTA"] = resposta
                respostas["MSÉ"] = resposta

                if resposta == "stop":
                    resposta = "Jogo encerrado. Obrigado por jogar!"
                    stop.set()
                #     break
                
                # conn.sendall(resposta.encode("utf-8"))

                print(f"[Server] Respondido para {addr}: {resposta}", flush=True)


    print(f"[Server] Conexão encerrada {addr}", flush=True)


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()

            thread = threading.Thread(
                target=atender_cliente,
                args=(conn, addr),
                daemon=True
            )
            thread.start()


if __name__ == "__main__":
    iniciar_servidor()