# 📌 Resumo para a prova: Sistemas Distribuídos (Aulas 01 a 03)

## 1. Processos (revisão)

- **Processo** = programa em execução (PC + pilha + dados + heap + código). Job ≈ processo.
- Memória do processo: **text** (código) · **data** (globais) · **heap** (dinâmica, cresce ↑) · **stack** (pilha, cresce ↓).
- **Estados:** novo → **pronto** ⇄ **executando** → terminado; executando → **esperando** (E/S/evento) → **pronto**. A interrupção leva de executando para **pronto**.
- **PCB:** estado, PID, PC, registradores, limites de memória, arquivos abertos.
- **Troca de contexto:** salva no PCB do processo que sai e carrega o PCB do que entra. É **overhead** (nenhum trabalho útil) e depende do hardware.
- **Filas:** de jobs (todos), de pronto (na memória, esperando a CPU), de dispositivo (esperando E/S).
- **Escalonador de longo prazo (job):** decide quem entra na fila de pronto; roda raramente; controla o **grau de multiprogramação**. **De curto prazo (CPU):** decide quem executa; roda a cada ms.
- **I/O-bound:** muitos bursts de CPU curtos. **CPU-bound:** poucos bursts longos.

## 2. Comunicação entre processos e corrida

- **Passagem de mensagens:** `send`/`receive`, sem variáveis compartilhadas; precisa de um link. **É a base dos SDs.**
- **Memória compartilhada:** rápida, mas exige sincronização.
- **Produtor-consumidor:** buffer **ilimitado** × **limitado** (o produtor espera se cheio, o consumidor espera se vazio).
- **Condição de corrida:** leitura e escrita concorrentes num dado compartilhado; o resultado **depende da ordem**. Difícil de depurar.
- **Região crítica** + **exclusão mútua (mutex)**. Quatro condições: (1) dois nunca ao mesmo tempo; (2) qualquer nº de CPUs e qualquer velocidade; (3) quem está fora não bloqueia; (4) ninguém espera para sempre.

## 3. Sistemas distribuídos

- **Definição (Tanenbaum):** computadores **autônomos** que trabalham juntos e parecem **um único sistema coerente**.
- **Objetivo:** **transparência**, ou seja, independência da estrutura de rede e de hardware.
- O usuário vê uma aplicação; o desenvolvedor vê **recursos de rede** (processamento, armazenamento, banda, BD, web).
- **Middleware:** camada de software "no meio", entre as aplicações e as plataformas, oferecendo uma API. Se está dentro do SO, a integração é maior.
- **Dificuldades:** SOs, representação de dados e padrões diferentes; limitações da rede.
- **Aplicações:** clusters (supercomputadores), web com milhares de usuários, bancos de dados, nuvem. **Exemplos:** Google, Gmail, Facebook, AWS.
- **Rede:** o SD depende dela (banda, latência); se a rede cai, o SD cai.

## 4. Arquiteturas (Aula 02)

- **ACID:** **A**tômica (tudo ou nada), **C**onsistente (respeita as regras), **I**solada (não interfere em outras transações), **D**urável (permanente após o commit).
- **Estilos:** em camadas · baseado em **objetos** (RPC) · em **eventos** (pub/sub) · em **dados** (repositório compartilhado).
- **3 camadas:** interface (cliente **magro** × **gordo**) · processamento (distribuído) · dados (**BD ativo**, com triggers/regras).
- **Centralizada** (cliente-servidor, papéis claros; ex.: Gmail) × **descentralizada** (P2P, todo nó é cliente e servidor; ex.: BitTorrent).
- **P2P estruturado = DHT:** hash do recurso e hash dos nós no **mesmo anel**; o recurso vai para o nó mais próximo (sucessor). Busca direta, sem inundação.
- **P2P não estruturado:** ligações aleatórias, vizinhos fixos, busca por **inundação**. **Superpeers:** mantêm índices e evitam rede desconexa (problema: como escolhê-los).
- **Híbrido = BitTorrent:** `.torrent` via servidor web (cliente-servidor) + DHT/pares (P2P).
- **Interceptador:** traduz a chamada da aplicação para o middleware.
- **Execução remota (A chama B em outra máquina), 3 fases:**
  1. **interface local**: **IDL** + **stub** (espelho local de B);
  2. **tradução pelo middleware**: formato geral, **serialização/marshalling**;
  3. **envio pela rede**: o SO cuida de roteamento e transporte; resposta **síncrona** ou **assíncrona**.

## 5. Sistemas de arquivos distribuídos (Aula 03)

- **De rede:** cada arquivo num servidor e o usuário **sabe qual** (NFS, SMB). **Distribuído:** arquivos espalhados em vários servidores, acessados **como locais**.
- **Montagem:** anexar um sistema de arquivos à árvore; depois dela, o arquivo remoto é usado como local.
- **5 características:**
  - **Transparência**: nomeação independente da localização;
  - **Escalabilidade**: novos clientes e servidores sem gargalo;
  - **Segurança**: permissões distribuídas; base de usuários central = gargalo;
  - **Tolerância a falhas**: detectar a falha, réplicas, **requisições idempotentes** (repetir = um único efeito);
  - **Consistência**: cache distribuído é complexo; **leitura compartilhada, escrita exclusiva**.
- **Atividade:** Ceph (RADOS, CRUSH, objeto/bloco/arquivo), JuiceFS (POSIX sobre object storage + motor de metadados), Storj (descentralizado, criptografado, erasure coding), Kertish-dfs (manager/head/data nodes, MongoDB, lock distribuído, mestre-escravo). Detalhes em [`aulas/03-.../atividade-pesquisa.md`](aulas/03-sistemas-arquivos-distribuidos/atividade-pesquisa.md).

## ✅ Checklist de véspera

- [ ] Desenho o diagrama de estados com as transições.
- [ ] Explico o PCB, a troca de contexto e por que ela é overhead.
- [ ] Diferencio os escalonadores de longo e curto prazo.
- [ ] Explico a condição de corrida com o exemplo da fila de impressão e as 4 condições da região crítica.
- [ ] Defino SD, transparência e middleware.
- [ ] Explico ACID com um exemplo.
- [ ] Explico DHT, inundação, superpeer e por que o BitTorrent é híbrido.
- [ ] Sei as 3 fases da execução remota (stub, IDL, serialização, síncrono/assíncrono).
- [ ] Diferencio FS de rede × distribuído e sei as 5 características.
- [ ] Sei dar exemplos de operações idempotentes e não idempotentes.
