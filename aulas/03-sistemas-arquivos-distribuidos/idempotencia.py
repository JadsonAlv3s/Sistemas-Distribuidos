"""Idempotência e tolerância a falhas.

Cenário: o cliente envia uma escrita, o servidor executa, mas a RESPOSTA se perde.
Sem saber se deu certo, o cliente REENVIA (retry). O que acontece com o arquivo?
Rode:  python idempotencia.py
"""


class ServidorDeArquivos:
    def __init__(self) -> None:
        self.conteudo = bytearray()

    def write_at(self, offset: int, dados: bytes) -> None:   # idempotente
        fim = offset + len(dados)
        if len(self.conteudo) < fim:
            self.conteudo.extend(b"\0" * (fim - len(self.conteudo)))
        self.conteudo[offset:fim] = dados

    def append(self, dados: bytes) -> None:                  # NÃO idempotente
        self.conteudo.extend(dados)


def enviar_com_retry(operacao, *args, resposta_perdida: bool) -> None:
    operacao(*args)                    # o servidor executa...
    if resposta_perdida:               # ...mas o "OK" não chega ao cliente
        print("    (timeout: o cliente não recebeu resposta e reenvia)")
        operacao(*args)                # retry


if __name__ == "__main__":
    for nome in ("write_at", "append"):
        srv = ServidorDeArquivos()
        op = getattr(srv, nome)
        args = (0, b"Ola!") if nome == "write_at" else (b"Ola!",)
        print(f"{nome}{args}:")
        enviar_com_retry(op, *args, resposta_perdida=True)
        print(f"    arquivo final = {bytes(srv.conteudo)!r}")
    print("\nwrite_at deu o mesmo resultado com 1 ou 2 envios (idempotente);")
    print("append duplicou o texto: não dá para repetir com segurança.")
