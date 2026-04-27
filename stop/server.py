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

# respostas = {}

# as mensagens [LOG] foram utilizadas para eu entender onde o programa estava.
 
stop = threading.Event() # Evento para controlar o encerramento do jogo
inicio_jogo = False


letra_sorteada = random.choice(string.ascii_letters) # Sorteia uma letra do alfabeto para o jogo  

n_jogadores = 5 #DEFINIR ANTES DE INICIAR

# Fila de mensagens
RESPOSTAS = [] # FILA
jogadores = {} # Tudo que é referente a jogadores foi armazenado aqui. 
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
    #with conn removido porque impedia a conexão de mais jogadores
    
# #print(f"[Server] Conexão encerrada {addr}", flush=True)
#     with conn:
#         # data = conn.recv(4096) 
#         # jogadores[conn]["nome"] = data.decode("utf-8").strip()    
#         #resposta = data.decode("utf-8") #guardo a resposta em resposta
#         print(f"[LOG] Jogo iniciado", flush=True)
#         if stop.is_set():
#             conn.sendall("Obrigado por jogar".encode('utf-8'))
        
        
        # while not stop.is_set():
        #     # Desenvolver jogo enquanto ninguem stoppou o jogo
        #     sleep(WAITING_TIME)
        #     if resposta == "stop":
        #         resposta = "Jogo encerrado. Obrigado por jogar!"
        #         stop.set()  
        #     conn.sendall(resposta.encode("utf-8"))
        #    print(f"[Server] Respondido para {addr}: {resposta}", flush=True)
            

#criada uma função iniciar jogo, para tratar as atividades após todos os jogadores se conectarem
def iniciar_jogo(jogadores):  
    print(f"[LOG] Etapa iniciar_jogo()")
    sleep(WAITING_TIME)
    # sorteio a letra e inicio o game
    print(f"[Server] Letra sorteada: {letra_sorteada}")
    
    #envio a letra sorteada a todos os jogadores online
    for jogador in jogadores.values():    
        print(f"[Server] Enviando letra sorteada para {jogador['nome']}", flush=True)
        print(f"[Server] jogo iniciado")
        jogador["conn"].sendall(f"Letra sorteada: {letra_sorteada}\n".encode("utf-8")) 
        jogador["conn"].sendall(f"JOGO INICIADO!!!!!!! \n".encode("utf-8"))    
        # problema! o ultimo jogador só recebe jogo iniciado [tratar].
        
        
        # tratar_respostas(jogador['conn'])
        
        # inicio a tratativa das respostas
        tratar_respostas_th = threading.Thread(
            target=tratar_respostas,
            args=(jogador,),
            daemon=True
        )
        
        tratar_respostas_th.start()
        
        # print(jogadores)
        
        # sleep(WAITING_TIME)
     
#criada uma função para receber as respostas dos temas   
def tratar_respostas(jogador): 
    global pontuacao # Inicio a variavel global; inicialmente não era, mas quando alterei a pontuação ser calculada após stop.set ela passou a dar erro de inexistencia.

    print(f"[LOG] Etapa tratar_respostas()")
    conn = jogador["conn"]
    nome_jogador = jogador["nome"]
    respostas_jogador = jogador["respostas"]
    # stop = jogador["respostas"]["STOP"]
    print(f"[Server] Tratando respostas do jogador {nome_jogador}")
    
    while not stop.is_set(): # enquanto não houve stop [stop não está setado]
        ### TRATANDO AS RESPOSTAS DOS TEMAS ###
        conn.sendall(f"NOME: ".encode("utf-8"))
        respostas = conn.recv(4096).decode("utf-8").strip()
        respostas_jogador["NOME"] = respostas  # GUARDA NO DICT
        recebeMensagem(respostas) # PRODUZ
        print(f"[Server] Jogador {nome_jogador} respondeu para [NOME]: {respostas_jogador['NOME']}", flush=True)
        
        # if stop.is_set():
        #     print('[LOG] Stop is true | interrompendo jogadores')
        #     break
        
        
        conn.sendall(f"FRUTA: ".encode("utf-8"))
        respostas = conn.recv(4096).decode("utf-8").strip()
        respostas_jogador["FRUTA"] = respostas # GUARDA NO DICT
        recebeMensagem(respostas) # PRODUZ
        print(f"[Server] Jogador {nome_jogador} respondeu para [FRUTA]: {respostas_jogador['FRUTA']}", flush=True)

        # if stop.is_set():
        #     print('[Server] Stop is true | interrompendo jogadores')
        #     break

        conn.sendall(f"CEP: ".encode("utf-8"))
        respostas = conn.recv(4096).decode("utf-8").strip()
        respostas_jogador["CEP"] = respostas  # GUARDA NO DICT
        recebeMensagem(respostas) # PRODUZ
        print(f"[Server] Jogador {nome_jogador} respondeu para [CEP]: {respostas_jogador['CEP']}", flush=True)
 
        # if stop.is_set():
        #     print('[Server] Stop is true | interrompendo jogadores')
        #     break
        
        conn.sendall(f"MSE: ".encode("utf-8"))
        respostas = conn.recv(4096).decode("utf-8").strip()
        respostas_jogador["MSE"] = respostas  # GUARDA NO DICT
        recebeMensagem(respostas) # PRODUZ
        print(f"[Server] Jogador {nome_jogador} respondeu para [MSE]: {respostas_jogador['MSE']}", flush=True)
        
        # if stop.is_set():
        #     print('[Server] Stop is true | interrompendo jogadores')
        #     break 
        
        # O jogador entra nesse if quando ele responde todos os temas
        if not stop.is_set():  
            print(f'[LOG] o jogador {nome_jogador} respondeu todos os temas')     
            # O que vai decidir quem ganha é quem envia 'stop' primeiro
            conn.sendall(f"VOCÊ RESPONDEU TUDO! ENVIE 'STOP' para encerrar o jogo: ".encode("utf-8")) 
            if conn.recv(4096).decode("utf-8").strip() == "stop": # jogador envia stop
                print(f"[LOG] O jogador {nome_jogador} enviou STOP!")
                stop.set()   # o stop é setado
                pontuacao = calcula_pontos(jogadores) # só vai entrar no calculo de pontos se existir um STOP, assim ficou mais facil para calcular pontos de forma única. [se não fosse dessa forma os pontos era calculados várias vezes]
                conn.sendall(f"Jogo encerrado por {nome_jogador}!\n".encode("utf-8"))
                print(f"[Server] Jogador {nome_jogador} enviou stop. Encerrando jogo...", flush=True)
                break # forço o encerramento do jogo
        else:
            conn.sendall(");\nOutro jogador respondeu stop primeiro!\nOs pontos estão sendo contados!".encode('utf-8'))
    print(f"[Server] Pontuação do jogador {nome_jogador} atualizada: {pontuacao}", flush=True)
    conn.sendall(f"Pontuação atualizada: {pontuacao}\n".encode("utf-8"))
    # print(jogadores)
    

# função de calcular pontos
def calcula_pontos(jogadores):
    print(f"[LOG] Etapa calcular_pontos()")
    print('[Server] calculando pontos | [LOG] STOP is true') # O esperado é que essa função seja iniciada apenas quando o stop estiver setado.
    print(f"[Server] Calculando pontos...")
    
    temas = ["NOME", "FRUTA", "CEP", "MSE"] # Criada uma lista de temas para contar as respostas ao TEMA de formas eparada
    for tema in temas: # Percorre a lista
        contagem_respostas = [] # Repostas serão armazenadas aqui unicamente.
        
        #contagem de respostas
        for jogador in jogadores.values():
            resposta = jogador["respostas"][tema].strip().lower() #sempre convertendo para minusculo para ficar mais facil a contagem
            
            # Tratando respostas vazias (temas que o usuario n conseguiu responder)
            if resposta == "": 
                continue
            
            contagem_respostas.append(resposta) # Atribui a resposta dentro da lista (contagem_respostas)
            
        print(f'[LOG] Tema: {tema}; Itens {contagem_respostas}')
        count = Counter(contagem_respostas)
        print(f'[LOG] {count}')
        
        # calculo de pontos
        if stop.is_set(): # Garantia que o Calculo só será feito após o primeiro STOP
            for jogador in jogadores.values():
                resposta = jogador["respostas"][tema].strip().lower()
                # se o usuario nao responder nada
                if resposta == '':
                    continue
                
                # Calculo dos pontos conforme passado na atividade
                elif count[resposta] == 1:
                    print(f'[LOG] {jogador["nome"]} ganhou 3 pontos no tema {tema}')
                    jogador["pontuacao"] += 3
                else:
                    print(f'[LOG] {jogador["nome"]} ganhou 1 ponto no tema {tema}')
                    jogador["pontuacao"] += 1
                
    # print(jogador["respostas"])
    
    # Informa o nome e a pontuação e envia aos usuários lá no tratar_respostas()
    return {
        jogador["nome"]: jogador["pontuacao"]
        for jogador in jogadores.values()
    }
        
    # pontuacao_atualizada = {jogador: jogadores[jogador]['pontuacao'] for jogador in jogadores}
    # return pontuacao_atualizada


def recebeMensagem(mensagem_cliente): #tread produtora  
    # tratando mensagens pós STOP
    if stop.is_set(): 
        print(f'[LOG] STOP is true [{mensagem_cliente}] ignorada')
    # Inclui RESPOSTAS na fila
    id_msg = 0
    print("[LOG] Produtor de mensagens inciado.", flush=True  )
    msg_produzida = f"{mensagem_cliente}"
    print(f"[Server] recebendo mensagem: '({msg_produzida})'", flush=True)
    produzir(msg_produzida.lower())
    id_msg += 1
    sleep(1)

# def enviaMensagem(): 
#     while True:
#         print(f"[LOG] Consumidor de mensagens inciado.", flush=True)
#         msg_enviada = consumir() # Retira a mensagem da fila,
#         for jogador in jogadores.values():
#             print(f"[Server] mensagem enviada: {msg_enviada}", flush=True)
#             conn = jogador["conn"]
#             conn.sendall(f"\n{msg_enviada}".encode("utf-8"))
#             print(f"[Server] Mensagens enviadas para {jogador['nome']}", flush=True)
#             # sleep(WAITING_TIME)
              
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

            # atribuo os jogadores e suas respostas ao dicionario criado no inicio.
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
            
            # iniciando o servico de atendimento com threads          
            thread = threading.Thread(
                target=atender_cliente,
                args=(conn, addr, nome),
                daemon=True 
            )
            print(f"[LOG] Jogador {nome} conectado. Total de jogadores: {len(jogadores)}")
            thread.start()

            # o jogo so inicia se tiver o número de jogadores cheio
            if len(jogadores) == n_jogadores:
                print(f"[LOG] Número de jogadores atingido.")
                # inicio_jogo = True
                iniciar_jogo_thread = threading.Thread(target=iniciar_jogo, args=(jogadores,), daemon=True)
                iniciar_jogo_thread.start()
                # print(f'Analisa dictionário de jogadores: {jogadores}')
            else:
                print(f"[LOG] Aguardando mais jogadores... {len(jogadores)}/{n_jogadores}")
                conn.sendall(f"Aguardando mais jogadores... {len(jogadores)}/{n_jogadores} \n".encode("utf-8"))



if __name__ == "__main__":
    iniciar_servidor()