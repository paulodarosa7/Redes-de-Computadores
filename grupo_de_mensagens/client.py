import socket

HOST = "127.0.0.1"
PORT = 9002

nome = input("[Cliente] Informe seu nome: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    cliente.sendall(nome.encode("utf-8"))
    
    while True:
        mensagem = input("O que você está pensando? ")
        cliente.sendall(mensagem.encode("utf-8"))
        cliente.recv(1024).decode("utf-8")