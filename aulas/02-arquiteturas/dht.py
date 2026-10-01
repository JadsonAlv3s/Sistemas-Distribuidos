"""DHT em anel (consistent hashing), como no slide "Peer to Peer".

- Nós e arquivos são colocados no MESMO espaço de chaves (o anel).
- Cada arquivo fica com o primeiro nó no sentido horário a partir do seu hash.
- Quando um nó entra, só as chaves vizinhas mudam de dono.
Rode:  python dht.py
"""
import bisect
import hashlib

TAMANHO_ANEL = 100   # espaço de chaves pequeno, para ficar fácil de ler


def h(nome: str) -> int:
    """Hash estável (SHA-1, igual em qualquer máquina) reduzido ao anel."""
    return int(hashlib.sha1(nome.encode()).hexdigest(), 16) % TAMANHO_ANEL


class AnelDHT:
    def __init__(self) -> None:
        self._posicoes: list[int] = []      # posições dos nós, ordenadas
        self._nos: dict[int, str] = {}      # posição -> nome do nó

    def adicionar_no(self, nome: str, posicao: int | None = None) -> None:
        pos = h(nome) if posicao is None else posicao
        bisect.insort(self._posicoes, pos)
        self._nos[pos] = nome

    def responsavel_por_chave(self, chave: int) -> str:
        """Sucessor: primeiro nó com posição >= chave; se passar do fim, dá a volta."""
        i = bisect.bisect_left(self._posicoes, chave)
        if i == len(self._posicoes):
            i = 0
        return self._nos[self._posicoes[i]]

    def responsavel(self, arquivo: str) -> str:
        return self.responsavel_por_chave(h(arquivo))

    def __str__(self) -> str:
        return " -> ".join(f"{self._nos[p]}@{p}" for p in self._posicoes) + " -> (volta)"


if __name__ == "__main__":
    # Exercício 8 do README: nós nas posições 10, 40, 75, 90
    anel = AnelDHT()
    for nome, pos in [("A", 10), ("B", 40), ("C", 75), ("D", 90)]:
        anel.adicionar_no(nome, pos)
    print("Anel:", anel)
    for chave in (5, 41, 80, 95):
        print(f"  chave {chave:2d} -> nó {anel.responsavel_por_chave(chave)}")

    # Distribuindo arquivos de verdade pelo hash do nome
    arquivos = ["aula01.pdf", "aula02.pdf", "aula03.pdf", "foto.png",
                "musica.mp3", "trabalho.docx", "video.mp4", "notas.txt"]
    antes = {a: anel.responsavel(a) for a in arquivos}
    print("\nArquivos (hash -> responsável):")
    for a in arquivos:
        print(f"  {a:14s} hash={h(a):2d} -> {antes[a]}")

    # Um nó novo entra: só quem está entre o antecessor dele e ele muda de dono
    anel.adicionar_no("E", 60)
    print("\nNó E entrou na posição 60. Anel:", anel)
    movidos = [a for a in arquivos if anel.responsavel(a) != antes[a]]
    print(f"Arquivos que mudaram de nó: {movidos or 'nenhum'}"
          f"  ({len(movidos)} de {len(arquivos)}; só as chaves entre 41 e 60)")
