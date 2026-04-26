import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = "127.0.0.1"
PORT = 9003

# Função para receber mensagens do servidor
def receber_mensagem():
    while True:
        try:
            data = cliente.recv(1024).decode("utf-8")
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"{data}\n")
            chat_area.yview(tk.END)  # rola até o fim
            chat_area.config(state='disabled')
            print(f"[LOG] Mensagem recebida!", flush=True)
        except:
            break

# Função para enviar mensagens
def enviar_mensagem():
    mensagem = msg_entry.get()
    print(f"[LOG] Sua mensagem foi enviada!", flush=True)
    if mensagem:
        cliente.sendall(mensagem.encode("utf-8"))
        msg_entry.delete(0, tk.END)

# Criando conexão
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

nome = input("[Cliente] Informe seu nome: ")
cliente.sendall(nome.encode("utf-8"))

# Criando interface Tkinter
root = tk.Tk()
root.title(f"Chat - {nome}")

# Área de mensagens
chat_area = scrolledtext.ScrolledText(root, state='disabled', width=100, height=20)
chat_area.pack(padx=10, pady=10)

# Campo de digitação
msg_entry = tk.Entry(root, width=90)
msg_entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
msg_entry.bind("<Return>", lambda event: enviar_mensagem())

# Botão de enviar
send_button = tk.Button(root, text="Enviar", command=enviar_mensagem)
send_button.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))

# Thread para receber mensagens
thread_recv = threading.Thread(target=receber_mensagem, daemon=True)
thread_recv.start()

root.mainloop()