# Aula 02: Conceitos e arquiteturas de sistemas distribuídos

> Slides: Aula02.pdf

## 1. Transações: ACID

Uma **transação** é um conjunto de operações tratado como uma unidade.

| Propriedade | Significado no slide | Exemplo (transferir R$ 100 de A para B) |
|---|---|---|
| **A**tômica | **indivisível** para o mundo exterior: tudo ou nada | ou debita de A **e** credita em B, ou nenhum dos dois |
| **C**onsistente | **não viola as regras** do sistema | a soma total de dinheiro não muda; saldo não fica negativo |
| **I**solada | **não afeta outras transações** concorrentes | quem consulta no meio do processo não vê "A debitado e B ainda não creditado" |
| **D**urável | depois de executada (*commit*), as alterações são **permanentes** | se o servidor cair logo depois, a transferência continua lá |

Num SD, a atomicidade é mais difícil: as operações estão em **máquinas diferentes**, e uma pode falhar no meio. (Protocolos como o *two-phase commit* resolvem isso; não estão no slide, mas é bom conhecer o nome.)

Demonstração: [`transacao_acid.py`](transacao_acid.py) faz uma transferência com SQLite e mostra o *rollback* quando ela falha no meio.

## 2. Estilos arquiteturais de SD

O slide só lista os estilos; a descrição abaixo segue o Tanenbaum.

| Estilo | Ideia | Exemplo |
|---|---|---|
| **Em camadas** | cada camada usa só a de baixo (requisição desce, resposta sobe) | modelo de rede TCP/IP; app → middleware → SO |
| **Baseado em objetos** | componentes são **objetos** que se chamam por **chamadas remotas** (RPC/RMI) | Java RMI, CORBA, gRPC |
| **Baseado em eventos** | componentes publicam e assinam **eventos** (publish/subscribe), **desacoplados** no tempo e no espaço | Kafka, MQTT, notificações |
| **Baseado em dados** | componentes se comunicam por um **repositório de dados compartilhado** | sistema de arquivos distribuído, banco compartilhado |

## 3. Arquitetura de aplicações em três camadas

| Camada | O que faz | Detalhe do slide |
|---|---|---|
| **Interface** (apresentação) | interação com o usuário | **clientes magros × gordos** |
| **Processamento** (lógica de negócio) | regras da aplicação | pode ser **distribuído** em vários servidores |
| **Dados** | armazenamento persistente | **bancos de dados ativos** |

- **Cliente magro (thin):** quase só exibe; o processamento fica no servidor (ex.: navegador acessando um sistema web). É fácil de manter e depende da rede.
- **Cliente gordo (fat/thick):** boa parte da lógica roda no cliente (ex.: aplicativo desktop, jogo). Alivia o servidor, mas é mais difícil de atualizar.
- **Banco de dados ativo:** o banco não só guarda dados, ele **reage a eventos** com regras e *triggers* (ex.: ao inserir uma venda, dar baixa no estoque automaticamente).

## 4. Centralizada × descentralizada

| | **Centralizada** (cliente-servidor) | **Descentralizada** (P2P) |
|---|---|---|
| Papéis | **separação clara**: muitos clientes usam serviços oferecidos por um conjunto de servidores | **sem separação clara**: todo nó pode ser cliente **e/ou** servidor |
| Exemplos | site web, Gmail, servidor de banco de dados | BitTorrent, blockchain |
| Ponto fraco | o servidor pode virar gargalo / ponto único de falha | localizar recursos é mais difícil |

## 5. P2P estruturado: DHT (Distributed Hash Table)

Os recursos são encontrados por um **processo padronizado**, quase sempre uma **DHT**:

1. Calcula-se um **hash (chave)** para cada **recurso** (ex.: o nome do arquivo).
2. O **mesmo espaço de chaves** nomeia os **nós** (hash do IP/ID do nó).
3. O espaço é visto como um **anel** (*continuum*).
4. Cada recurso fica no nó **mais próximo do seu hash**, normalmente o **primeiro nó no sentido horário** (o "sucessor").
5. Para achar um arquivo, basta calcular o hash do nome e perguntar ao nó responsável. **Não precisa inundar a rede.**

```
           node a
        ●─────────●
   node d          │      um arquivo → HASH → cai entre c e b
      ●            ●      → o responsável é o próximo nó no sentido do anel (node b)
      │   anel     │
   node c ●───────● node b
```

**Vantagem extra:** quando um nó entra ou sai, só as chaves **vizinhas** a ele mudam de lugar (é o *consistent hashing*).

Demonstração: [`dht.py`](dht.py) monta o anel, distribui arquivos e mostra o que acontece quando um nó entra.

## 6. P2P não estruturado e superpeers

**Não estruturado:**
- as ligações entre os nós são **aleatórias**;
- cada nó conhece um **número fixo de vizinhos**;
- para buscar um dado, o nó **inunda a rede** (*flooding*): pergunta aos vizinhos, que repassam aos vizinhos deles, até achar.
- É simples, mas gera muito tráfego e não garante encontrar o recurso (normalmente há um limite de saltos, o TTL).

**Superpeers (superpares):**
- nós com **papel diferente**, normalmente com mais recursos e estabilidade;
- mantêm **índices** que interligam outros nós (buscas mais rápidas);
- **evitam que a rede não estruturada fique desconexa**;
- problema: **como escolher** quem vira superpar? (É um problema de eleição.)

## 7. Redes híbridas: o BitTorrent

Combinam vários modelos:
1. **Cliente-servidor:** o usuário baixa o arquivo **`.torrent`** de um **servidor web**.
2. O `.torrent` contém o **hash** do arquivo desejado (e dos pedaços).
3. **P2P:** com o hash, o cliente usa a **DHT** para achar os pares que têm o arquivo e baixa os pedaços **deles**.

## 8. Interceptadores

- Muitos middlewares se baseiam em **objetos remotos** e **RPC** (*Remote Procedure Call*).
- **Interceptador** = camada que **intercepta o pedido da aplicação e o traduz para o middleware**. O middleware então o traduz para o SD e o executa na máquina de destino.
- Dá para pensar nele como um "desvio" colocado no caminho da chamada: a aplicação chama como se fosse local e o interceptador redireciona para o objeto remoto (pode também acrescentar coisas como replicação, log ou segurança).

## 9. Execução remota (RPC / objetos remotos)

**Definição:** o objeto **A** chama um método do objeto **B**, que está em **outra máquina**. Três fases:

### 1. Interface local
- O objeto que oferece serviços **publica a interface** dos métodos públicos numa **IDL** (*Interface Definition Language*), que é neutra em relação à linguagem.
- A partir da IDL, A cria um **stub**: um objeto **local** que é **espelho** do objeto remoto B.
- A chama o stub como se fosse B, e o stub converte a chamada para o **formato geral de requisição**.

### 2. Tradução pelo middleware
- O middleware define o **formato geral** das requisições na rede.
- A requisição é traduzida para esse formato.
- Aqui se resolvem **representação e serialização** dos dados (**marshalling**: transformar parâmetros em bytes; ex.: JSON, XML, Protocol Buffers).

### 3. Envio pela rede
- Usa o mecanismo de rede da máquina local; **roteamento e transporte** ficam com o **SO** (TCP/IP).
- Depois de enviar, é preciso **aguardar a resposta**:
  - **síncrono:** A **bloqueia** até a resposta chegar;
  - **assíncrono:** A **continua** executando e trata a resposta depois (callback/future).

> Do lado do servidor, o par do stub costuma se chamar **skeleton**: ele recebe a requisição, faz o *unmarshalling* e chama o método real de B.

```
 Máquina 1                                      Máquina 2
 A ──► stub(B) ──► middleware ──► rede ──► middleware ──► skeleton ──► B
   (chamada local)  (serializa)   (SO/TCP)  (desserializa)  (chama de verdade)
```

Demonstração: [`rpc_stub.py`](rpc_stub.py) roda um servidor e um cliente RPC (XML-RPC da biblioteca padrão). O cliente chama `calc.somar(2, 3)` como se fosse local.

---

## Atividade do slide (respondida)

<details><summary><b>1. Defina middleware.</b></summary>

Camada de software que fica **entre as aplicações e os sistemas operacionais/rede** das várias máquinas de um SD. Ela oferece uma **API uniforme** e esconde a heterogeneidade (SOs, representação de dados, protocolos), dando **transparência** de distribuição. Ex.: middlewares de RPC/objetos remotos (gRPC, Java RMI, CORBA) e de mensagens (RabbitMQ, Kafka).
</details>

<details><summary><b>2. Qual a função de um interceptador de chamadas no SD?</b></summary>

Interceptar a chamada feita pela aplicação, como se fosse local, e **traduzi-la para o middleware**, que a converte em requisição do SD e a executa na máquina de destino. Assim a aplicação não precisa saber que o objeto é remoto. O interceptador também pode adicionar comportamentos sem mudar a aplicação (replicação, log, autenticação).
</details>

<details><summary><b>3. Descreva o funcionamento de uma DHT.</b></summary>

Tabela hash distribuída entre os nós de uma rede P2P estruturada. Uma função hash gera uma chave para cada recurso, e o **mesmo espaço de chaves** identifica os nós, organizados num anel. Cada recurso fica no nó cujo identificador está mais próximo da sua chave (o sucessor no anel). Para buscar, calcula-se o hash do recurso e a consulta é roteada até o nó responsável, sem inundar a rede. Quando um nó entra ou sai, só as chaves vizinhas são realocadas.
</details>

<details><summary><b>4. Diferença entre arquitetura centralizada e descentralizada, com exemplos.</b></summary>

**Centralizada:** papéis bem separados. Muitos clientes consomem serviços de um conjunto de servidores. Ex.: Gmail, um site web, um servidor de banco de dados.
**Descentralizada:** não há separação clara; cada nó pode ser cliente e servidor ao mesmo tempo. Ex.: BitTorrent, redes blockchain.
</details>

## Exercícios extras

1. Explique cada letra do ACID com o exemplo de uma compra num e-commerce (pagamento + baixa no estoque).
2. Classifique quanto ao estilo arquitetural: (a) um sistema de chat com publish/subscribe; (b) uma chamada gRPC; (c) vários serviços lendo/gravando num mesmo banco.
3. Cliente magro ou gordo: (a) Google Docs no navegador; (b) um jogo instalado no PC; (c) um terminal bancário que só exibe telas.
4. Por que a busca numa rede P2P não estruturada é cara? Como os superpeers ajudam?
5. Por que o BitTorrent é chamado de híbrido?
6. O que é stub? O que é IDL? O que é marshalling/serialização?
7. Diferença entre chamada síncrona e assíncrona. Dê um exemplo de quando a assíncrona é melhor.
8. No anel de uma DHT com nós nas posições 10, 40, 75 e 90 (espaço 0–99), quem guarda chaves de hash 5, 41, 80 e 95?

<details><summary><b>Respostas</b></summary>

1. **A:** cobra e dá baixa, ou nenhum dos dois. **C:** o estoque nunca fica negativo e o valor cobrado bate com o pedido. **I:** dois clientes comprando a última unidade não "veem" o mesmo estoque ao mesmo tempo. **D:** confirmado o pedido, ele não se perde se o servidor cair.
2. (a) baseado em eventos; (b) baseado em objetos (RPC); (c) baseado em dados.
3. (a) magro; (b) gordo; (c) magro.
4. Porque a consulta é inundada (*flooding*) por toda a rede, multiplicando mensagens, e nem garante encontrar. Superpeers mantêm índices: a consulta vai a eles em vez de passar por todos os nós, e eles mantêm a rede conectada.
5. Porque usa cliente-servidor (baixar o `.torrent` de um servidor web) e P2P (DHT e troca de pedaços entre pares).
6. **Stub:** objeto local que é espelho do objeto remoto e transforma a chamada em requisição. **IDL:** linguagem neutra para descrever a interface (métodos e tipos) do objeto remoto. **Marshalling:** converter parâmetros/resultados num formato transmissível (bytes) e de volta.
7. Síncrona: quem chama bloqueia até a resposta. Assíncrona: continua e trata a resposta depois. Melhor quando a operação é demorada e o chamador pode fazer outra coisa (ex.: gerar um relatório pesado, enviar e-mail, interface que não pode travar).
8. Sucessor no sentido horário: 5 → **10**; 41 → **75**; 80 → **90**; 95 → dá a volta → **10**. Confira rodando `python dht.py`.
</details>
