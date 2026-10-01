# Simulado: Sistemas Distribuídos (Aulas 01 a 03)

**Tempo sugerido:** 50 min. Gabarito no final.

## Parte A: múltipla escolha

**1.** Um processo que terminou uma operação de E/S vai para o estado:
a) executando · b) pronto · c) novo · d) terminado

**2.** Qual informação NÃO costuma estar no PCB?
a) contador de programa · b) registradores · c) lista de arquivos abertos · d) código-fonte do programa

**3.** O escalonador invocado a cada poucos milissegundos é o:
a) de longo prazo · b) de jobs · c) de curto prazo · d) de dispositivos

**4.** "O resultado final depende da ordem em que os processos são executados" define:
a) deadlock · b) condição de corrida · c) troca de contexto · d) starvation

**5.** Na passagem de mensagens:
a) os processos compartilham variáveis · b) usa-se send/receive · c) não é necessário um link · d) só funciona na mesma máquina

**6.** A camada de software que fica entre as aplicações e as plataformas de um SD é o:
a) kernel · b) stub · c) middleware · d) escalonador

**7.** "Uma vez executada, as alterações são permanentes" é a propriedade:
a) atomicidade · b) consistência · c) isolamento · d) durabilidade

**8.** Numa DHT, um recurso é alocado:
a) ao primeiro nó que responder · b) ao nó mais próximo do seu hash · c) a todos os nós · d) ao superpeer

**9.** A busca por inundação é característica de:
a) P2P estruturado · b) P2P não estruturado · c) cliente-servidor · d) DHT

**10.** O objeto local que é espelho do objeto remoto chama-se:
a) IDL · b) stub · c) interceptador · d) PCB

**11.** Num sistema de arquivos **de rede**:
a) o usuário não sabe onde está o arquivo · b) o usuário precisa conhecer o servidor · c) cada arquivo fica em vários servidores · d) não há montagem

**12.** Qual operação é idempotente?
a) append no fim do arquivo · b) incrementar contador · c) escrever bytes no offset 0 · d) criar arquivo com nome sequencial

## Parte B: discursivas

**13.** Explique, passo a passo, como duas tarefas enviadas à fila de impressão podem fazer um arquivo sumir. Como evitar?

**14.** Por que passagem de mensagens é a forma natural de IPC num sistema distribuído?

**15.** Descreva as 3 fases da execução remota de um método de B a partir de A.

**16.** Explique por que o BitTorrent é híbrido e o papel do hash nesse processo.

**17.** Um cliente fez uma escrita, o servidor caiu e o cliente não sabe se a escrita foi feita. Como a idempotência resolve isso?

**18.** Dois clientes querem abrir o mesmo arquivo de um sistema de arquivos distribuído. Descreva o que pode e o que não pode acontecer ao mesmo tempo, e por quê.

---

<details><summary><b>Gabarito</b></summary>

1-b · 2-d · 3-c · 4-b · 5-b · 6-c · 7-d · 8-b · 9-b · 10-b · 11-b · 12-c

13. P1 lê `inicio=3` e é tirado da CPU; P2 lê o mesmo 3; P2 grava seu arquivo na posição 3 e grava inicio=4; P1 volta, grava o dele também na posição 3 (sobrescreve) e grava inicio=4. Um arquivo sumiu. Solução: tratar ler/gravar/incrementar como **região crítica** protegida por **exclusão mútua (mutex)**.

14. Porque máquinas diferentes não compartilham memória. A única forma de cooperar é trocar mensagens pela rede (send/receive), que é o que RPC, objetos remotos e middlewares fazem por baixo.

15. (1) **Interface local:** B publica sua interface numa IDL; A cria um **stub** (espelho local de B) e chama o método nele. (2) **Middleware:** a chamada é traduzida para o formato geral de requisição, com **serialização** dos parâmetros. (3) **Rede:** o pedido é enviado pelo mecanismo de rede local (o SO cuida de roteamento/transporte) e A aguarda a resposta de forma **síncrona** ou **assíncrona**.

16. Primeiro usa **cliente-servidor**: baixa o `.torrent` de um servidor web. Esse arquivo contém o **hash** do conteúdo. Depois usa **P2P**: com o hash, consulta a **DHT** para achar os pares que têm o arquivo e baixa os pedaços deles. O hash identifica o recurso na DHT.

17. Se a operação é idempotente (ex.: "escreva estes bytes na posição X"), o cliente simplesmente **reenvia** a mesma requisição (a outro servidor/réplica ou quando o servidor voltar). Executar uma ou duas vezes dá o mesmo resultado, sem duplicar dados.

18. Se os dois só **leem**, podem acessar simultaneamente (leitura compartilhada). Se um deles **escreve**, ele precisa de acesso **exclusivo**, para evitar condição de corrida e leituras de dados inconsistentes. Também é preciso cuidar do **cache**, para que ninguém leia uma cópia desatualizada.
</details>
