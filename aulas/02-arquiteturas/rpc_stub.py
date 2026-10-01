"""Execução remota (RPC) com a biblioteca padrão: xmlrpc.

Servidor: expõe o objeto B (Calculadora).
Cliente:  cria um STUB (ServerProxy) e chama calc.somar(2, 3) como se fosse local.
Por baixo: o stub serializa (marshalling) a chamada em XML, envia por HTTP/TCP,
o servidor desserializa, executa e devolve a resposta (chamada SÍNCRONA).
Rode:  python rpc_stub.py   (sobe o servidor numa thread e o cliente usa)
"""
import threading
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer


class Calculadora:                      # o "objeto B" que mora no servidor
    def somar(self, a: int, b: int) -> int:
        return a + b

    def dividir(self, a: float, b: float) -> float:
        return a / b


class HandlerSilencioso(SimpleXMLRPCRequestHandler):
    def log_message(self, *args) -> None:  # não poluir a saída
        pass


def iniciar_servidor() -> SimpleXMLRPCServer:
    servidor = SimpleXMLRPCServer(("127.0.0.1", 0), requestHandler=HandlerSilencioso,
                                  allow_none=True)
    servidor.register_instance(Calculadora())        # publica a interface
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


if __name__ == "__main__":
    servidor = iniciar_servidor()
    porta = servidor.server_address[1]

    calc = xmlrpc.client.ServerProxy(f"http://127.0.0.1:{porta}")   # STUB
    print("calc.somar(2, 3) =", calc.somar(2, 3))                   # parece local!

    # O que o stub manda pela rede (marshalling da chamada):
    print("\nRequisição serializada pelo stub:")
    print(xmlrpc.client.dumps((2, 3), methodname="somar"))

    # Erros remotos voltam como exceção no cliente (transparência... até certo ponto)
    try:
        calc.dividir(1, 0)
    except xmlrpc.client.Fault as erro:
        print("Erro vindo do servidor:", erro.faultString)

    servidor.shutdown()
