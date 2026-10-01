# Questões de autoteste (Aulas 01 a 03)

<details><summary><b>1.</b> Defina processo. O que ele inclui?</summary>
Programa em execução. Inclui contador de programa, pilha, seção de dados (e heap e código na memória), além do estado mantido no PCB.
</details>

<details><summary><b>2.</b> Quais os 5 estados de um processo?</summary>
Novo, pronto, executando, esperando e terminado.
</details>

<details><summary><b>3.</b> O que leva um processo de executando para pronto? E para esperando?</summary>
Para pronto: interrupção (ex.: fim da fatia de tempo). Para esperando: pedido de E/S ou espera por um evento.
</details>

<details><summary><b>4.</b> O que é a troca de contexto e por que ela é overhead?</summary>
Salvar o estado do processo atual no PCB dele e carregar o do próximo a partir do PCB deste. Durante a troca, a CPU não faz trabalho útil.
</details>

<details><summary><b>5.</b> Qual escalonador controla o grau de multiprogramação?</summary>
O de longo prazo (de jobs), porque decide quantos e quais processos entram na fila de pronto.
</details>

<details><summary><b>6.</b> Diferencie fila de jobs, fila de pronto e fila de dispositivo.</summary>
Jobs: todos os processos do sistema. Pronto: os que estão na memória principal esperando a CPU. Dispositivo: os que esperam por um dispositivo de E/S.
</details>

<details><summary><b>7.</b> Quais as duas formas de comunicação entre processos?</summary>
Passagem de mensagens (send/receive, sem variáveis compartilhadas) e memória compartilhada.
</details>

<details><summary><b>8.</b> O que é condição de corrida?</summary>
Situação em que processos leem e escrevem um dado compartilhado e o resultado final depende da ordem de execução.
</details>

<details><summary><b>9.</b> Quais as 4 condições para uma boa solução de região crítica?</summary>
(1) Dois processos nunca simultaneamente na região crítica; (2) funcionar com qualquer número de CPUs e velocidade; (3) processo fora da região crítica não bloqueia outros; (4) nenhum processo espera eternamente.
</details>

<details><summary><b>10.</b> Defina sistema distribuído.</summary>
Conjunto de computadores autônomos que trabalham juntos para dar a aparência de um único sistema coerente.
</details>

<details><summary><b>11.</b> O que é middleware?</summary>
Camada de software entre as aplicações e as plataformas (SO/rede) das várias máquinas, que oferece os serviços do SD por uma API e esconde a heterogeneidade.
</details>

<details><summary><b>12.</b> O que é um cluster?</summary>
Um aglomerado de várias máquinas (de médio porte) que trabalham como um único sistema. É como são feitos a maioria dos supercomputadores atuais.
</details>

<details><summary><b>13.</b> Explique o ACID.</summary>
Atômica: indivisível (tudo ou nada). Consistente: não viola as regras do sistema. Isolada: não afeta outras transações. Durável: depois de executada, as alterações são permanentes.
</details>

<details><summary><b>14.</b> Quais os 4 estilos arquiteturais citados?</summary>
Em camadas, baseado em eventos, baseado em dados e baseado em objetos.
</details>

<details><summary><b>15.</b> Cliente magro × cliente gordo?</summary>
Magro: quase só interface, o processamento fica no servidor (ex.: app web). Gordo: grande parte da lógica roda no cliente (ex.: aplicativo desktop).
</details>

<details><summary><b>16.</b> Arquitetura centralizada × descentralizada?</summary>
Centralizada: separação clara entre muitos clientes e um conjunto de servidores (ex.: Gmail). Descentralizada: todo nó pode ser cliente e/ou servidor (ex.: BitTorrent).
</details>

<details><summary><b>17.</b> Como funciona uma DHT?</summary>
Calcula-se o hash de cada recurso; o mesmo espaço de chaves nomeia os nós (anel); o recurso fica no nó mais próximo do seu hash. A busca é direta, calculando o hash.
</details>

<details><summary><b>18.</b> Como é feita a busca num P2P não estruturado?</summary>
Por inundação: o nó pergunta aos vizinhos, que repassam aos vizinhos deles, até achar o recurso.
</details>

<details><summary><b>19.</b> Para que servem os superpeers?</summary>
Nós com papel diferenciado que mantêm índices interligando outros nós e evitam que a rede não estruturada fique desconexa. Problema: como selecioná-los.
</details>

<details><summary><b>20.</b> Por que o BitTorrent é uma rede híbrida?</summary>
Usa cliente-servidor para obter o .torrent (que contém o hash do arquivo) num servidor web e depois P2P (DHT/pares) para baixar o arquivo.
</details>

<details><summary><b>21.</b> O que faz o interceptador?</summary>
Traduz o pedido da aplicação para o middleware, que o traduz para o SD e o executa na máquina de destino.
</details>

<details><summary><b>22.</b> Quais as 3 fases da execução remota?</summary>
Interface local (IDL + stub), tradução pelo middleware (formato geral, serialização) e transformação em pedido de rede (envio pelo SO, resposta síncrona ou assíncrona).
</details>

<details><summary><b>23.</b> O que é stub? E IDL?</summary>
Stub: objeto local que é espelho do objeto remoto e converte a chamada em requisição. IDL: linguagem de definição de interface, que descreve os métodos públicos do objeto remoto.
</details>

<details><summary><b>24.</b> Síncrono × assíncrono?</summary>
Síncrono: quem chama espera bloqueado pela resposta. Assíncrono: continua executando e trata a resposta quando ela chegar.
</details>

<details><summary><b>25.</b> Sistema de arquivos de rede × distribuído?</summary>
De rede: cada arquivo está num servidor e o usuário precisa conhecer o nome do servidor. Distribuído: arquivos espalhados por vários servidores, acessados como se fossem locais.
</details>

<details><summary><b>26.</b> O que é montagem?</summary>
Anexar um novo sistema de arquivos à árvore de diretórios (conceito Unix). Depois de montado, um arquivo da rede é usado como local.
</details>

<details><summary><b>27.</b> Quais as 5 características importantes de um sistema de arquivos distribuído?</summary>
Transparência, escalabilidade, segurança, tolerância a falhas e consistência.
</details>

<details><summary><b>28.</b> O que a transparência exige?</summary>
Um serviço de nomeação independente da localização física, para que o usuário não precise saber em que servidor(es) o arquivo está.
</details>

<details><summary><b>29.</b> O que é uma requisição idempotente? Por que ajuda?</summary>
Várias requisições iguais geram um único efeito. Permite reenviar com segurança quando não se sabe se o pedido anterior foi executado (ex.: resposta perdida, servidor caiu).
</details>

<details><summary><b>30.</b> Qual a regra de acesso concorrente para manter a consistência?</summary>
Leitura pode ser compartilhada; escrita deve ser exclusiva.
</details>
