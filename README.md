# Projetos Cliente/Servidor com Threads e Semáforos (Trabalho TADS - Redes de Computadores)

## 📌 Sobre o repositório

Este repositório contém **duas atividades distintas** relacionadas à implementação de sistemas cliente/servidor utilizando **Python, sockets, threads e controle de concorrência**.

Cada atividade foi desenvolvida com foco em conceitos específicos de comunicação em rede e sincronização, sendo organizadas em diretórios separados.

---

## 📁 Estrutura do repositório

O repositório está dividido em diretórios, onde cada um contém uma atividade completa:

```
├── grupo_de_mensagens
│   ├── server.py
│   └── client.py
└── stop
    ├── server.py
    └── client.py
```

> ⚠️ **Importante:**
> Cada diretório possui seu próprio `README.md` com instruções detalhadas de execução e uso.

---

## 🧠 Conceitos abordados

As atividades exploram:

* Comunicação cliente-servidor via sockets TCP
* Atendimento simultâneo de múltiplos clientes com threads
* Sincronização de acesso a recursos compartilhados
* Problema produtor-consumidor
* Uso de semáforos para controle de concorrência
* Estruturação de sistemas distribuídos simples

---

## 🧩 Atividade 1 — Jogo Stop (Cliente/Servidor)

Implementação de um jogo estilo **Stop**, onde múltiplos clientes se conectam ao servidor e participam de uma rodada.

### Características:

* Controle de múltiplos jogadores
* Comunicação em tempo real
* Encerramento do jogo via comando STOP
* Cálculo de pontuação baseado nas respostas
* Uso de threads para tratamento simultâneo

---

## 💬 Atividade 2 — Chat com Fila e Semáforos

Implementação de um sistema de chat com múltiplos clientes.

### Características:

* Fila de mensagens compartilhada
* Controle de acesso com semáforos
* Threads produtoras e consumidoras
* Envio de mensagens para todos os clientes conectados
* Interface gráfica utilizando Tkinter

---

## ⚙️ Tecnologias utilizadas

* Python 3
* Sockets (TCP)
* Threading
* Semáforos
* Tkinter (interface gráfica, atividade de chat)

---

## 🚀 Execução

Cada atividade possui suas próprias instruções de execução.

👉 Acesse o diretório desejado e siga o arquivo:

```text
README.md
```

---

## ⚠️ Observações gerais

* Os sistemas foram desenvolvidos para **uso acadêmico**
* Podem apresentar limitações em cenários reais ou com desconexões inesperadas
* Recomenda-se executar os testes de forma controlada

---

## 📌 Boas práticas

* Sempre iniciar o servidor antes dos clientes
* Utilizar nomes/identificações ao conectar
* Evitar interromper execuções abruptamente
* Reiniciar o servidor ao iniciar novos testes
* Evite palavras com caracteres especiais e acentuação como [ç ´ ` ~ { ? # $ % ¨ ! \ ) ( } e outros]

---

## 🎓 Finalidade

Este repositório tem como objetivo consolidar conhecimentos em:

* Programação concorrente
* Redes de computadores
* Sincronização de processos
* Arquitetura cliente-servidor

---

## 👤 Autor

Desenvolvido por: *Paulo Henrique e Wuesley Soares*
Curso: *ADS*
Disciplina: *Redes de Computadores*
