# Jogo Stop - Cliente/Servidor

## Descrição

Este projeto implementa um jogo do tipo "Stop" utilizando comunicação via sockets em Python. O sistema é dividido em servidor e cliente, onde múltiplos jogadores se conectam e participam da mesma partida.

## Estrutura dos arquivos

* `server.py` → Responsável por gerenciar conexões, fluxo do jogo e pontuação
* `client.py` → Responsável pela interação do jogador com o servidor

## Requisitos

* Python 3 instalado

## Execução

### 1. Iniciar o servidor

No terminal:

```
python3 server.py
```

O servidor será iniciado no endereço:

```
0.0.0.0:9002
```

### 2. Iniciar os clientes

Em outros terminais (um para cada jogador):

```
python3 client.py
```

## Funcionamento do jogo

* O servidor aguarda a conexão de **5 jogadores**
* Após atingir esse número, o jogo inicia automaticamente
* Uma letra é sorteada
* Os jogadores devem responder aos seguintes temas:

  * Nome
  * Fruta
  * CEP
  * MSE
* Após responder todos os temas, o jogador pode digitar **STOP** para encerrar o jogo
* O primeiro jogador que enviar STOP encerra a rodada
* O servidor então calcula a pontuação

## Sistema de pontuação

* Resposta única (ninguém mais respondeu igual): **3 pontos**
* Resposta repetida: **1 ponto**
* Respostas vazias: **0 pontos**

⚠️ **Importante:**
O sistema **não verifica se as palavras começam com a letra sorteada**.
Ele apenas realiza o cálculo e tratamento das respostas informadas pelos jogadores.

## Limitações

* O jogo funciona corretamente apenas com **5 jogadores**
* Não há validação das respostas em relação à letra sorteada
* Não há tratamento robusto para desconexões inesperadas
* O fluxo depende do cliente seguir corretamente a ordem das respostas
* Pode ocorrer bloqueio caso algum jogador não responda

## Como utilizar corretamente

* Inicie o servidor antes dos clientes
* Conecte exatamente com o número de jogadores especificado em **n_jogadores**
* Responda todos os temas conforme solicitado
* Após responder tudo, envie **STOP** para finalizar o jogo
* Não interrompa o cliente durante a execução 

## Observações

Este projeto tem fins acadêmicos e demonstra conceitos de:

* Programação com sockets
* Concorrência com threads
* Sincronização com semáforos
* Comunicação cliente-servidor
* O teste foi feito com no máximo 5 jogadores
