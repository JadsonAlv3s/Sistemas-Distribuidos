# Sistemas-Distribuidos

Material de estudo de **Sistemas Distribuídos** (TSI / IFRN), organizado a partir dos slides das aulas, com explicações, exercícios resolvidos e **demonstrações em Python** que mostram os conceitos funcionando.

## 🚀 Estudando para a prova? Siga esta ordem

1. **[RESUMO-PROVA.md](RESUMO-PROVA.md)**: as 3 aulas numa página, com checklist de véspera.
2. **[questoes-teoricas.md](questoes-teoricas.md)**: 30 perguntas de autoteste (respostas escondidas).
3. **[Simulado](simulados/simulado-1.md)**: 12 de múltipla escolha + 6 discursivas, com gabarito.

## 📚 Aulas

| # | Tema | Demonstrações |
|---|---|---|
| 01 | [Processos, IPC, condição de corrida e conceitos de SD](aulas/01-processos-e-conceitos/) | `condicao_corrida.py` · `produtor_consumidor.py` · `passagem_mensagens.py` |
| 02 | [Arquiteturas: ACID, centralizada × P2P, DHT, RPC/stub](aulas/02-arquiteturas/) | `transacao_acid.py` · `dht.py` · `rpc_stub.py` |
| 03 | [Sistemas de arquivos distribuídos](aulas/03-sistemas-arquivos-distribuidos/) + [atividade de pesquisa (Ceph, JuiceFS, Storj, Kertish-dfs)](aulas/03-sistemas-arquivos-distribuidos/atividade-pesquisa.md) | `idempotencia.py` |

Cada pasta tem um `README.md` com a teoria, a atividade do slide respondida e exercícios com respostas.

## ▶️ Rodando as demonstrações

Python 3.10+, só a biblioteca padrão (nada para instalar).

```bash
python aulas/01-processos-e-conceitos/condicao_corrida.py    # perde arquivos sem mutex; com mutex, não
python aulas/02-arquiteturas/dht.py                          # anel da DHT e entrada de um nó
python aulas/02-arquiteturas/rpc_stub.py                     # chamada remota via stub
python aulas/03-sistemas-arquivos-distribuidos/idempotencia.py
```

Todas foram executadas e rodam sem erro.
