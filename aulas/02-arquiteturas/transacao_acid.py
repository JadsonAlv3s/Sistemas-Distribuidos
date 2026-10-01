"""Atomicidade e consistência numa transferência bancária (SQLite).

A transferência tem dois passos: debitar A e creditar B.
Se algo falhar no meio, o ROLLBACK desfaz o débito: tudo ou nada.
Rode:  python transacao_acid.py
"""
import sqlite3


def criar_banco() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE conta (nome TEXT PRIMARY KEY, saldo REAL CHECK (saldo >= 0))")
    con.executemany("INSERT INTO conta VALUES (?, ?)", [("A", 500.0), ("B", 100.0)])
    con.commit()
    return con


def saldos(con: sqlite3.Connection) -> dict[str, float]:
    return dict(con.execute("SELECT nome, saldo FROM conta ORDER BY nome"))


def transferir(con: sqlite3.Connection, origem: str, destino: str, valor: float,
               falhar_no_meio: bool = False) -> None:
    try:
        with con:  # inicia a transação: commit no fim, rollback se der exceção
            con.execute("UPDATE conta SET saldo = saldo - ? WHERE nome = ?", (valor, origem))
            if falhar_no_meio:
                raise ConnectionError("servidor caiu entre o débito e o crédito")
            con.execute("UPDATE conta SET saldo = saldo + ? WHERE nome = ?", (valor, destino))
        print(f"  OK: {origem} -> {destino} R$ {valor:.2f}")
    except (ConnectionError, sqlite3.IntegrityError) as erro:
        print(f"  FALHOU ({erro}); rollback feito")


if __name__ == "__main__":
    con = criar_banco()
    print("Início:", saldos(con), "| total =", sum(saldos(con).values()))

    print("1) transferência normal")
    transferir(con, "A", "B", 200)
    print("  ", saldos(con))

    print("2) falha no meio (Atomicidade)")
    transferir(con, "A", "B", 100, falhar_no_meio=True)
    print("  ", saldos(con), "<- o débito foi desfeito")

    print("3) saldo insuficiente (Consistência: CHECK saldo >= 0)")
    transferir(con, "A", "B", 9999)
    print("  ", saldos(con))

    print("Fim: total =", sum(saldos(con).values()), "(nunca mudou: dinheiro não sumiu nem surgiu)")
