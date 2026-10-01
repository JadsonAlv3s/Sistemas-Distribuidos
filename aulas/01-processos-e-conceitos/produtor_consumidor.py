"""Produtor-consumidor com BUFFER LIMITADO.

O aplicativo (produtor) gera documentos; a impressora (consumidor) imprime.
queue.Queue(maxsize=N) já faz a sincronização: put() bloqueia com o buffer
cheio e get() bloqueia com o buffer vazio.  Rode:  python produtor_consumidor.py
"""
import queue
import threading
import time

TAMANHO_BUFFER = 2
FIM = None                                   # sentinela: "não há mais nada"


def produtor(buffer: queue.Queue, n: int) -> None:
    for i in range(1, n + 1):
        doc = f"documento-{i}"
        if buffer.full():
            print(f"[produtor]   buffer cheio, esperando para enviar {doc}")
        buffer.put(doc)                      # bloqueia se cheio
        print(f"[produtor]   enviou {doc}  (ocupação {buffer.qsize()}/{TAMANHO_BUFFER})")
    buffer.put(FIM)


def consumidor(buffer: queue.Queue) -> None:
    while True:
        doc = buffer.get()                   # bloqueia se vazio
        if doc is FIM:
            print("[consumidor] fim da fila")
            break
        time.sleep(0.05)                     # imprimir é mais lento que produzir
        print(f"[consumidor] imprimiu {doc}")


if __name__ == "__main__":
    buffer: queue.Queue = queue.Queue(maxsize=TAMANHO_BUFFER)
    tc = threading.Thread(target=consumidor, args=(buffer,))
    tp = threading.Thread(target=produtor, args=(buffer, 5))
    tc.start(); tp.start()
    tp.join(); tc.join()
