# Aula 01: Revisão de processos, comunicação entre processos e conceitos de SD

> Slides: Aula01.pdf (IFRN 2024.2)

## Parte 1: Processos (revisão de SO)

### 1.1 O que é um processo

- **Processo = um programa em execução.** O programa é o arquivo parado no disco; o processo é ele rodando, com estado.
- A execução de um processo progride de modo **sequencial**.
- Em sistemas *batch* se fala em **jobs**; em sistemas de tempo compartilhado, em programas/tarefas. **Job e processo costumam ser sinônimos.**
- Um processo inclui, entre outras coisas: **contador de programa** (PC, a próxima instrução), **pilha** e **seção de dados**.

### 1.2 Processo na memória

```
max ┌──────────┐
    │  stack   │  pilha: chamadas de função, variáveis locais (cresce ↓)
    │    ↓     │
    │          │  espaço livre
    │    ↑     │
    │  heap    │  memória alocada dinamicamente (malloc/new) (cresce ↑)
    │  data    │  variáveis globais/estáticas
    │  text    │  o código (instruções)
  0 └──────────┘
```

### 1.3 Estados de um processo

| Estado | Significado |
|---|---|
| **Novo** (*new*) | está sendo criado |
| **Pronto** (*ready*) | esperando para ser atribuído a um processador |
| **Executando** (*running*) | instruções sendo executadas |
| **Esperando** (*waiting*) | esperando algum evento (E/S, sinal) |
| **Terminado** (*terminated*) | terminou a execução |

```
 new ──admitted──► ready ──scheduler dispatch──► running ──exit──► terminated
                    ▲  ◄────────interrupt─────────  │
                    │                               │ I/O or event wait
                    └──I/O or event completion── waiting ◄┘
```

> ⚠️ Pegadinha: de **esperando** o processo vai para **pronto**, nunca direto para executando. E **interrupção** (fim da fatia de tempo) leva de executando para **pronto**, não para esperando.

### 1.4 Troca de contexto e PCB

- **PCB (Process Control Block)** guarda tudo sobre o processo: **estado, número (PID), contador de programa, registradores, limites de memória, lista de arquivos abertos**...
- **Troca de contexto:** quando a CPU passa para outro processo, o SO **salva o estado do antigo no PCB dele** e **carrega o estado do novo a partir do PCB dele**.
- O tempo de troca é **overhead**: o sistema não faz trabalho útil nesse intervalo. Depende do **suporte do hardware**.
- **Quando acontece?** Pedido de E/S, fim da fatia de tempo (*time slice expired*), criação de filho (*fork*), espera por interrupção, chamada de sistema.

### 1.5 Filas de processos

| Fila | Contém |
|---|---|
| **Fila de jobs** | **todos** os processos do sistema |
| **Fila de pronto** | processos **na memória principal**, prontos, esperando a CPU |
| **Filas de dispositivo** | processos esperando por um dispositivo de E/S (uma fila por dispositivo) |

Os processos **migram** entre as filas. As filas são listas encadeadas de PCBs (*head/tail*).

### 1.6 Escalonador

Programa/algoritmo que **ordena as filas** de processos.

| | Longo prazo (**de job**) | Curto prazo (**de CPU**) |
|---|---|---|
| Decide | **quais processos entram na fila de pronto** | **qual processo executa em seguida** e aloca a CPU |
| Frequência | **raramente** (segundos, minutos) | **muito frequente** (milissegundos) |
| Controla | o **grau de multiprogramação** (quantos processos na memória) | o uso da CPU |

Tipos de processo:
- **Voltados para E/S (I/O-bound):** mais tempo em E/S que em cálculo; *bursts* de CPU **curtos**.
- **Voltados para CPU (CPU-bound):** mais tempo calculando; **poucos** *bursts* **longos**.

Um bom escalonador de longo prazo **mistura** os dois tipos para não deixar a CPU nem os dispositivos ociosos.

## Parte 2: Comunicação entre processos (IPC)

SOs modernos são multitarefa, e alguns processos precisam **cooperar** (ex.: um aplicativo mandando um documento para o processo de impressão). Duas formas:

| | **Passagem de mensagens** | **Memória compartilhada** |
|---|---|---|
| Como | `send(destino, msg)` / `receive(origem, msg)`, via kernel | uma região de memória acessível aos dois |
| Variáveis compartilhadas? | **Não** | **Sim** |
| Vantagens | simples de sincronizar; **funciona entre máquinas** (é a base dos SDs) | rápida (sem passar pelo kernel a cada troca) |
| Riscos | custo de cópia/chamadas de sistema | **condição de corrida**: exige sincronização |

Para P e Q trocarem mensagens: **(1)** estabelecer um link de comunicação e **(2)** trocar mensagens com send/receive.

### Problema do produtor-consumidor

O **produtor** gera informações que o **consumidor** usa (ex.: aplicativo → fila de impressão).
- **Buffer ilimitado:** sem limite prático; o produtor nunca espera.
- **Buffer limitado:** tamanho fixo; o produtor **espera** se cheio e o consumidor **espera** se vazio.

Demonstração: [`produtor_consumidor.py`](produtor_consumidor.py) e [`passagem_mensagens.py`](passagem_mensagens.py).

## Parte 3: Condição de corrida e região crítica

**Condição de corrida (race condition):** dois processos **leem e escrevem** um dado compartilhado e o **resultado final depende da ordem** em que executam. Como num SO multitarefa um processo pode sair de *executando* para *pronto* **a qualquer momento**, a falha é intermitente, **muito difícil de depurar** e depende de fatores externos.

**Exemplo do slide (fila de impressão):**
```
P1: ler(inicio)           → lê 3
                             P2: ler(inicio)            → lê 3 também!
P1: pilha[3] = arqA
P1: incrementa; grava 4
                             P2: pilha[3] = arqB        → SOBRESCREVE arqA
                             P2: incrementa; grava 4
Resultado: arqA sumiu e inicio = 4 (deveria ser 5).
```

**Região crítica** = trecho do código que acessa o recurso compartilhado.
**Solução:** **exclusão mútua (mutex)**, ou seja, impedir que mais de um processo leia/escreva ao mesmo tempo. **É dever do programador** identificar e proteger essas regiões.

**As 4 condições para uma boa solução:**
1. Dois processos **não podem estar simultaneamente** na região crítica.
2. Deve funcionar para **qualquer número de CPUs e qualquer velocidade** (nada de supor tempos).
3. Nenhum processo **fora** da região crítica pode **bloquear** outros.
4. Nenhum processo deve **esperar eternamente** para entrar (sem *starvation*).

Demonstração: [`condicao_corrida.py`](condicao_corrida.py) reproduz o exemplo do slide e o corrige com mutex.

## Parte 4: Sistemas distribuídos, conceitos iniciais

> **"Um sistema distribuído consiste de um conjunto de computadores autônomos que trabalham juntos para dar a aparência de um único sistema coerente."** (Tanenbaum)

- **Objetivo principal:** dar ao usuário uma visão **transparente** e **independente** da estrutura de rede e de hardware.
- Uma **camada de software** obtém essa transparência:
  - o **usuário** vê só uma aplicação executando remotamente;
  - o **desenvolvedor** vê um **recurso de rede**: processamento, armazenamento, largura de banda, banco de dados, serviços web.

### Middleware

- A camada que oferece os serviços do SD aparece como uma **biblioteca/API** para os desenvolvedores.
- Pode estar **no próprio SO** (mais integração) ou **separada**. Quando é separada, chama-se **middleware**: *"o software que está no meio"*, entre as aplicações e as várias plataformas (SOs/máquinas).

```
 Aplicação 1   Aplicação 2   Componente
 ─────────── API ──────────────────────
   Middleware: serviços do SD
 ──────────────────────────────────────
 Plataforma 1   Plataforma 2   Plataforma 3
```

### Por que é difícil construir um SD

Integrar totalmente sistemas com **SOs diferentes**, **representação de dados diferente** (ex.: *endianness*, tamanho de inteiros, codificação de texto), **padrões de codificação e comunicação diferentes** e **limitações da rede**.

### Aplicações e exemplos

- **Alto poder de processamento:** antes eram máquinas enormes de propósito único; hoje a maioria dos supercomputadores é um **cluster** (aglomerado de máquinas de médio porte).
- **Agrupar** aplicações que rodam em computadores diferentes num único sistema.
- **Escalar** sem mexer nas aplicações (crescimento das redes e da nuvem).
- Exemplos: servidores web com milhares de usuários simultâneos, bancos de dados, aplicações em nuvem, **Google, Gmail, Facebook, Amazon AWS** (data centers espalhados pelo mundo).

### SD e as redes

- SDs **surgiram com as redes** e são **altamente dependentes** delas.
- Devem **abstrair as diferenças** entre redes e oferecer uma **comunicação uniforme**.
- **Banda e latência** são questões centrais.
- Se a rede para, o SD para. Os benefícios **e as limitações** do SD vêm do funcionamento da rede.

---

## Exercícios

1. Qual a diferença entre programa e processo?
2. Desenhe o diagrama de estados e diga o que causa cada transição.
3. Um processo em *esperando* pode ir direto para *executando*? Por quê?
4. O que o PCB armazena e qual o papel dele na troca de contexto?
5. Por que a troca de contexto é chamada de *overhead*?
6. Compare o escalonador de longo e o de curto prazo (decisão, frequência, o que controla).
7. Um editor de texto e um programa que renderiza vídeo: qual é I/O-bound e qual é CPU-bound?
8. Compare passagem de mensagens e memória compartilhada. Qual delas é natural num sistema distribuído?
9. Explique o problema produtor-consumidor com buffer limitado.
10. Defina condição de corrida e descreva, passo a passo, como a fila de impressão do slide perde um arquivo.
11. O que é região crítica e exclusão mútua? Cite as 4 condições de uma boa solução.
12. Defina sistema distribuído e explique "transparência".
13. O que é middleware? Onde ele fica?
14. Cite 3 dificuldades de construir um SD.
15. Por que se diz que os benefícios e as limitações de um SD estão ligados à rede?

<details><summary><b>Respostas</b></summary>

1. Programa é o código parado (arquivo); processo é o programa **em execução**, com PC, pilha, dados e estado próprios.
2. new →(admitido) ready →(despacho do escalonador) running; running →(interrupção/fim da fatia) ready; running →(espera por E/S ou evento) waiting; waiting →(E/S ou evento concluído) ready; running →(exit) terminated.
3. Não. Ao concluir a E/S ele volta para **pronto**; quem decide quem executa é o escalonador de curto prazo.
4. Estado, PID, contador de programa, registradores, limites de memória, arquivos abertos. Na troca, o SO salva o contexto do processo que sai no PCB dele e recarrega o do processo que entra a partir do PCB dele.
5. Porque, enquanto salva/carrega contextos, a CPU não executa trabalho útil de nenhum processo.
6. Longo prazo: escolhe quais processos entram na fila de pronto; roda raramente (s/min); controla o grau de multiprogramação. Curto prazo: escolhe quem usa a CPU agora; roda a cada poucos ms.
7. Editor de texto: I/O-bound (espera teclado/disco). Renderização: CPU-bound.
8. Mensagens: sem variáveis compartilhadas, send/receive via kernel, funciona entre máquinas. Memória compartilhada: rápida, mas exige sincronização. Em SD, **passagem de mensagens**, porque máquinas diferentes não compartilham memória.
9. O produtor coloca itens num buffer de tamanho fixo e o consumidor retira. Se o buffer está cheio, o produtor espera; se está vazio, o consumidor espera. É preciso sincronizar o acesso ao buffer.
10. Resultado depende da ordem de execução. P1 lê `inicio=3` e é interrompido; P2 lê o mesmo 3; os dois gravam na posição 3 (um sobrescreve o outro) e ambos gravam `inicio=4`. Um arquivo some.
11. Região crítica é o trecho que acessa o dado compartilhado; exclusão mútua garante que só um processo esteja nela por vez. Condições: não dois ao mesmo tempo; sem suposições sobre CPUs/velocidade; quem está fora não bloqueia; ninguém espera para sempre.
12. Computadores autônomos que cooperam e parecem um único sistema coerente. Transparência = o usuário não percebe a distribuição (onde estão os recursos, quantas máquinas, falhas...).
13. Camada de software entre as aplicações e as plataformas (SOs/hardware), que oferece os serviços do SD por meio de uma API.
14. SOs diferentes; representação de dados diferente; padrões de codificação/comunicação diferentes; limitações da rede (banda, latência, falhas).
15. Toda cooperação passa pela rede: se ela falha ou fica lenta, o SD falha ou fica lento; a escalabilidade e o alcance também vêm dela.
</details>
