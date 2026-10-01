"""Passagem de mensagens entre DOIS PROCESSOS de verdade (não threads).

Os processos P e Q não compartilham variáveis: cada um tem sua própria memória.
Eles se comunicam por um link (Pipe) usando send/receive, como no slide.
Rode:  python passagem_mensagens.py
"""
import os
from multiprocessing import Pipe, Process

contador = 0          # cada processo tem a SUA cópia desta variável


def processo_q(link) -> None:
    global contador
    while True:
        msg = link.recv()                          # receive(origem, mensagem)
        if msg == "FIM":
            break
        contador += 1
        link.send(f"Q (pid {os.getpid()}) recebeu '{msg}' (contador de Q = {contador})")


if __name__ == "__main__":
    ponta_p, ponta_q = Pipe()                       # 1) estabelecer o link
    q = Process(target=processo_q, args=(ponta_q,))
    q.start()
    for texto in ["olá", "imprime isso", "tchau"]:   # 2) trocar mensagens
        ponta_p.send(texto)                          # send(destino, mensagem)
        print(f"P (pid {os.getpid()}) <- {ponta_p.recv()}")
    ponta_p.send("FIM")
    q.join()
    print(f"contador em P continua {contador}: não há memória compartilhada")
