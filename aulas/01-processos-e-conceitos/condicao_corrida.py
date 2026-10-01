"""Condição de corrida na fila de impressão (exemplo do slide) e a correção com mutex.

Duas threads fazem o mesmo trecho do slide:
    ler(inicio); pilha[inicio] = arquivo; incrementa(inicio); gravaNovoInicio()
Entre ler e gravar forçamos uma troca de contexto (time.sleep), como o SO faria
num momento qualquer. Rode:  python condicao_corrida.py
"""
import threading
import time


class FilaImpressao:
    def __init__(self) -> None:
        self.pilha: list[str | None] = [None] * 50
        self.inicio = 3                          # já existem Arq1..Arq3
        self.pilha[0:3] = ["Arq1.txt", "Arq2.txt", "Arq3.txt"]
        self.mutex = threading.Lock()

    def enfileirar_sem_protecao(self, arquivo: str) -> None:
        posicao = self.inicio                    # ler(inicio)
        time.sleep(0.001)                        # o SO tira o processo da CPU aqui
        self.pilha[posicao] = arquivo            # pilha[inicio] = arquivo
        self.inicio = posicao + 1                # incrementa + grava novo início

    def enfileirar_com_mutex(self, arquivo: str) -> None:
        with self.mutex:                         # entra na REGIÃO CRÍTICA
            self.enfileirar_sem_protecao(arquivo)
                                                 # sai e libera o mutex


def rodar(metodo: str) -> None:
    fila = FilaImpressao()
    threads = [threading.Thread(target=getattr(fila, metodo), args=(f"Doc{i}.txt",))
               for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    arquivos = [a for a in fila.pilha if a]
    print(f"{metodo}:")
    print(f"  inicio = {fila.inicio} (esperado 8)")
    print(f"  arquivos na fila = {len(arquivos)} (esperado 8) -> {arquivos}")


if __name__ == "__main__":
    rodar("enfileirar_sem_protecao")   # perde documentos: todos gravam na posição 3
    rodar("enfileirar_com_mutex")      # correto: um de cada vez na região crítica
