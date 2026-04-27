# Chat Cliente/Servidor com Threads e Semáforos

## Descrição

Este projeto implementa um chat cliente/servidor utilizando sockets em Python.

O servidor é responsável por gerenciar as conexões dos clientes, receber mensagens, armazená-las em uma fila e reenviá-las aos clientes conectados. O acesso à fila é controlado por semáforos, evitando acesso concorrente.

O cliente utiliza Tkinter apenas como interface visual para envio e recebimento das mensagens.

## Arquivos

* `server.py`
  Código responsável pelo gerenciamento das conexões com os clientes e gerenciamento das mensagens.

* `client.py`
  Código executado pelo cliente. Ele permite enviar mensagens e também receber as mensagens do servidor pela interface gráfica.

* `README.md`
  Arquivo com as instruções de execução.

## Porta utilizada

O servidor executa na porta:

```text
9003
```

Endereço do servidor:

```text
0.0.0.0:9003
```

No cliente, para testes locais, é utilizado:

```text
127.0.0.1:9003
```

## Requisitos

* Python 3 instalado
* Tkinter disponível no ambiente Python

## Como executar

### 1. Iniciar o servidor

Abra um terminal e execute:

```bash
python3 server.py
```

O servidor ficará aguardando conexões na porta `9003`.

### 2. Iniciar os clientes

Para cada cliente, abra um novo terminal e execute:

```bash
python3 client.py
```

Ao iniciar, o cliente solicitará um nome:

```text
[Cliente] Informe seu nome:
```

Digite um nome ou username para identificar o usuário no chat.

## Como utilizar corretamente

* Inicie primeiro o servidor.
* Depois, abra um cliente por vez.
* Cada cliente deve informar um nome ou username.
* Não feche a janela do cliente enquanto estiver utilizando o chat.
* Envie uma mensagem por vez.
* As mensagens recebidas aparecerão na área principal da tela.
* Para encerrar um teste, finalize o servidor e todos os clientes.
* Caso algum teste seja interrompido, reinicie o servidor antes de conectar novos clientes.

## Funcionamento

1. O servidor é iniciado e fica aguardando conexões.
2. O cliente se conecta ao servidor.
3. Antes de enviar mensagens, o cliente envia seu nome ao servidor.
4. O servidor armazena os dados do cliente conectado.
5. Cada cliente conectado é atendido por uma thread.
6. Quando uma mensagem é recebida, o servidor coloca essa mensagem em uma fila.
7. O acesso à fila é protegido por semáforos.
8. Threads consumidoras retiram mensagens da fila.
9. As mensagens são enviadas para os clientes conectados.

As mensagens exibidas contêm:

* Nome do cliente
* IP e porta da conexão
* Horário em que o servidor recebeu a mensagem
* Conteúdo da mensagem

## Observação sobre os arquivos

A atividade solicita arquivos separados para envio e recebimento no cliente. Neste projeto, essas duas funções foram implementadas em um único arquivo de cliente porque foi utilizada interface gráfica com Tkinter.

Dentro do `client.py`, o envio e o recebimento acontecem de forma separada:

* o envio ocorre pela função responsável por capturar o texto digitado e enviar ao servidor;
* o recebimento ocorre por uma thread separada, que escuta mensagens do servidor e atualiza a tela.

## Limitações

* O servidor não trata bem novas conexões após desconexões inesperadas.
* Caso um cliente seja fechado durante o teste, o ideal é parar o servidor e todos os clientes antes de testar novamente.
* Não há tratamento completo para remoção de clientes desconectados.
* O sistema deve ser usado de forma regrada, com cada cliente informando um nome ou username.
* O Tkinter foi utilizado apenas para facilitar a visualização das mensagens.
* O sistema foi testado considerando uso local com `127.0.0.1`.
* As mensagens com acentuação não conseguiram ser bem tratadas - Evite mensagens com acentos

## Encerramento recomendado

Para parar um teste:

1. Feche todos os clientes.
2. Pare o servidor no terminal.
3. Inicie novamente o servidor.
4. Abra novamente os clientes.

Esse procedimento evita problemas com conexões antigas ou clientes desconectados.
