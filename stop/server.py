from concurrent.futures import thread
from collections import Counter
import socket
import threading
import random
import json
import string
from time import sleep

HOST = "0.0.0.0"
PORT = 9002

WAITING_TIME = 2

respostas = {}



stop = threading.Event() # Evento para controlar o encerramento do jogo
inicio_jogo = False



n_jogadores = 2 #DEFINIR ANTES DE INICIAR

# Fila de mensagens
RESPOSTAS = []
jogadores = {}

# # Semáforo de acesso à fila
SEMAFORO_ACESSO = threading.Semaphore(1) # Apenas 1 thread pode acessar a fila por vez

# Quantidade de itens. Quem insere na fila, incrementa. Quem consome, decrementa.
SEMAFORO_ITENS = threading.Semaphore(0)  # A fila inicia com 0 elementos

def produzir(mensagem):
    global RESPOSTAS
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Inclui a mensagem na fila
    RESPOSTAS.append(mensagem)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Informa que há itens na fila.
    SEMAFORO_ITENS.release() 

def consumir():
    global RESPOSTAS
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda até que existam itens na fila
    SEMAFORO_ITENS.acquire()

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Verifica se há mensagens na fila
    if RESPOSTAS:
        # Retira a primeira mensagem da fila
        mensagem = RESPOSTAS.pop(0)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Retorna a mensagem que estava na fila
    return mensagem


def atender_cliente(conn, addr, nome):   
    print(f"[Server] Encontrando jogadores...")
    # Recebendo jogadores
    conn.sendall(f"{nome} seja bem-vindo ao meu servidor! \n".encode("utf-8"))
    print(f"[Server] Nova conexão {addr}", flush=True)
    conn.sendall(b"Vamos jogar stop! \n")
#print(f"[Server] Conexão encerrada {addr}", flush=True)
    # with conn:
    #     data = conn.recv(4096) 
    #     jogadores[conn]["nome"] = data.decode("utf-8").strip()    
    #     resposta = data.decode("utf-8") #guardo a resposta em resposta
    #     print(f"[LOG] Jogo iniciado", flush=True)
        
    #     while not stop.is_set():
    #         # Desenvolver jogo enquanto ninguem stoppou o jogo
    #         sleep(WAITING_TIME)
    #         if resposta == "stop":
    #             resposta = "Jogo encerrado. Obrigado por jogar!"
    #             stop.set()  
            # conn.sendall(resposta.encode("utf-8"))
            # print(f"[Server] Respondido para {addr}: {resposta}", flush=True)
            
            
def iniciar_jogo(jogadores):  
    print(f"[LOG] Etapa iniciar_jogo()")
    sleep(WAITING_TIME)
    letra_sorteada = random.choice(string.ascii_letters) # Sorteia uma letra do alfabeto para o jogo  
    print(f"[LOG] Letra sorteada: {letra_sorteada}")
    for jogador in jogadores.values():    
        print(f"[Server] Enviando letra sorteada para {jogador['nome']}", flush=True)
        print(f"[Server] jogo iniciado")
        jogador["conn"].sendall(f"Letra sorteada: {letra_sorteada}\n".encode("utf-8"))
        jogador["conn"].sendall(f"JOGO INICIADO!!!!!!! \n".encode("utf-8"))    
        
        
        
        # tratar_respostas(jogador['conn'])
        
        tratar_respostas_th = threading.Thread(
            target=tratar_respostas,
            args=(jogador,),
            daemon=True
        )
        
        tratar_respostas_th.start()
        
        # sleep(WAITING_TIME)
        
def tratar_respostas(jogador):
    print(f"[LOG] Etapa tratar_respostas()")
    conn = jogador["conn"]
    nome_jogador = jogador["nome"]
    respostas_jogador = jogador["respostas"]
    # stop = jogador["respostas"]["STOP"]
    print(f"[LOG] Tratando respostas do jogador {nome_jogador}")
    
    while not stop.is_set():
        conn.sendall(f"NOME: ".encode("utf-8"))
        respostas = conn.recv(4096).decode("utf-8").strip()
        respostas_jogador["NOME"] = respostas
        recebeMensagem(respostas)
        print(f"[LOG] Jogador {nome_jogador} respondeu para [NOME]: {respostas_jogador['NOME']}", flush=True)
        
        conn.sendall(f"FRUTA: ".encode("utf-8"))
        respostas = conn.recv(4096).decode("utf-8").strip()
        respostas_jogador["FRUTA"] = respostas
        recebeMensagem(respostas)
        print(f"[LOG] Jogador {nome_jogador} respondeu para [FRUTA]: {respostas_jogador['FRUTA']}", flush=True)

        conn.sendall(f"CEP: ".encode("utf-8"))
        respostas = conn.recv(4096).decode("utf-8").strip()
        respostas_jogador["CEP"] = respostas
        recebeMensagem(respostas)
        print(f"[LOG] Jogador {nome_jogador} respondeu para [CEP]: {respostas_jogador['CEP']}", flush=True)
        
        conn.sendall(f"MSE: ".encode("utf-8"))
        respostas = conn.recv(4096).decode("utf-8").strip()
        respostas_jogador["MSE"] = respostas
        recebeMensagem(respostas)
        print(f"[LOG] Jogador {nome_jogador} respondeu para [MSE]: {respostas_jogador['MSE']}", flush=True)
        
        conn.sendall(f"VOCÊ RESPONDEU TUDO! ENVIE 'STOP' para encerrar o jogo: ".encode("utf-8"))
        if conn.recv(4096).decode("utf-8").strip() == "stop":
            stop.set()
            
    conn.sendall(f"Jogo encerrado por {nome_jogador}!\n".encode("utf-8"))
    print(f"[LOG] Jogador {nome_jogador} enviou stop. Encerrando jogo...", flush=True)
    
    pontuacao =calcula_pontos(jogadores)
    
    print(f"[LOG] Pontuação do jogador {nome_jogador} atualizada: {pontuacao}", flush=True)
    conn.sendall(f"Pontuação atualizada: {pontuacao}\n".encode("utf-8"))

def calcula_pontos(jogadores):
    print(f"[LOG] Etapa calcular_pontos()")
    print('[Server] calculando pontos | [LOG] STOP is true')
    print(f"[LOG] Calculando pontos...")
    
    temas = {
        "NOME": {}, # jogador[nome] : resposta = 1
        "FRUTA": {},
        "CEP": {},
        "MSE": {}
    }

    for tema in temas:
        contagem_respostas = []
        
        for jogador in jogadores.values():
            resposta = jogador["respostas"][tema].strip().lower()
            contagem_respostas.append(resposta)
            
        count = Counter(contagem_respostas)
        
        for jogador in jogadores.values():
            resposta = jogador["respostas"][tema].strip().lower()
            if count[resposta] == 1:
                print(f'[LOG] {jogador["nome"]} ganhou 3 pontos no tema {tema}')
                jogador["pontuacao"] += 3
            else:
                print(f'[LOG] {jogador["nome"]} ganhou 1 ponto no tema {tema}')
                jogador["pontuacao"] += 1
                
    return {
        jogador["nome"]: jogador["pontuacao"]
        for jogador in jogadores.values()
    }

    
    
                
    
            
         
    
    

        
    pontuacao_atualizada = {jogador: jogadores[jogador]['pontuacao'] for jogador in jogadores}
    return pontuacao_atualizada


def recebeMensagem(mensagem_cliente): #tread produtora  
    # Inclui RESPOSTAS na fila
    id_msg = 0
    print("[LOG] Produtor de mensagens inciado.", flush=True  )
    msg_produzida = f"{mensagem_cliente}"
    print(f"[Server] recebendo mensagem: '({msg_produzida})'", flush=True)
    produzir(msg_produzida)
    id_msg += 1
    sleep(1)

def enviaMensagem(): 
    while True:
        print(f"[LOG] Consumidor de mensagens inciado.", flush=True)
        msg_enviada = consumir() # Retira a mensagem da fila,
        for jogador in jogadores.values():
            print(f"[Server] mensagem enviada: {msg_enviada}", flush=True)
            conn = jogador["conn"]
            conn.sendall(f"\n{msg_enviada}".encode("utf-8"))
            print(f"[Server] Mensagens enviadas para {jogador['nome']}", flush=True)
            # sleep(WAITING_TIME)
              


# def calcula_pontos(jogadores):
#     sleep(WAITING_TIME)
#     print(f"[LOG] Calculando pontos...")
    
#     for jogador in jogadores.values():
#         print(f"Jogador: {jogador}, Respostas: {jogadores[jogador]['respostas']}")
#         if jogadores[jogador]['respostas']['NOME'] == jogador['respostas']['NOME'] and jogadores[jogador]['respostas']['FRUTA'] == jogador['respostas']['FRUTA'] and jogadores[jogador]['respostas']['CEP'] == jogador['respostas']['CEP'] and jogadores[jogador]['respostas']['MSÉ'] == jogador['respostas']['MSÉ']:
#             jogadores[jogador]['pontuacao'] += 1
#         else:
#             jogadores[jogador]['pontuacao'] += 3
            
#     pontuacao_atualizada = {jogador: jogadores[jogador]['pontuacao'] for jogador in jogadores}
#     return pontuacao_atualizada
        
        
def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while True: # DEFINIR QUANDO INICIAR O JOGO
            conn, addr = server.accept()
            nome = conn.recv(4096).decode("utf-8") # recebe o nome do cliente

            jogadores[conn] = {
                "nome": nome, 
                "conn": conn,
                "addr": addr,  
                "pontuacao": 0,
                # "IP": addr,
                "respostas": {
                    "NOME": "",
                    "FRUTA": "",
                    "CEP": "",
                    "MSE": "",
                    # "STOP": threading.Event(),
                    
                }
            }
            
            
            
            thread = threading.Thread(
                target=atender_cliente,
                args=(conn, addr, nome),
                daemon=True 
            )
            print(f"[LOG] Jogador {nome} conectado. Total de jogadores: {len(jogadores)}")
            thread.start()

            
            if len(jogadores) == n_jogadores:
                print(f"[LOG] Número de jogadores atingido.")
                inicio_jogo = True
                iniciar_jogo_thread = threading.Thread(target=iniciar_jogo, args=(jogadores,), daemon=True)
                iniciar_jogo_thread.start()
                print(f'Analisa dictionário de jogadores: {jogadores}')
            else:
                print(f"[LOG] Aguardando mais jogadores... {len(jogadores)}/{n_jogadores}")
                conn.sendall(f"Aguardando mais jogadores... {len(jogadores)}/{n_jogadores} \n".encode("utf-8"))



if __name__ == "__main__":
    iniciar_servidor()