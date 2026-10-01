# Atividade: Kertish-dfs, JuiceFS, Storj e Ceph

> Atividade da Aula 03: *"Pesquisar e descrever os seguintes sistemas de arquivos distribuídos."*
> Use como base de estudo e **confira os detalhes na documentação oficial** antes de entregar. Esses projetos evoluem, e a entrega deve ter suas palavras e suas fontes.

## Ceph

- **O que é:** plataforma de armazenamento distribuído **open source** (LGPL), muito usada em data centers e nuvens privadas (OpenStack, Proxmox).
- **Armazenamento unificado:** um mesmo cluster oferece
  - **objetos** (RADOS Gateway, compatível com **S3**/Swift),
  - **blocos** (RBD, discos virtuais para VMs),
  - **arquivos** (**CephFS**, sistema de arquivos POSIX montável).
- **Arquitetura:** tudo roda sobre o **RADOS** (*Reliable Autonomic Distributed Object Store*):
  - **OSD** (*Object Storage Daemon*): um por disco; guarda os dados, replica e se recupera;
  - **MON** (*Monitor*): mantém o mapa do cluster (em número ímpar, por quórum);
  - **MGR** (*Manager*): métricas e painel;
  - **MDS** (*Metadata Server*): metadados do CephFS.
- **Ponto-chave: algoritmo CRUSH.** O cliente **calcula** onde um objeto está, a partir do mapa do cluster, **sem consultar uma tabela central**. Não há gargalo de localização (mesma ideia da DHT da Aula 02).
- **Tolerância a falhas:** **replicação** (ex.: 3 cópias) ou **erasure coding**; quando um disco ou nó cai, o cluster se **auto-recupera** (rebalanceia as cópias).
- **Relação com a aula:** transparência (o cliente não sabe em que OSD está o dado), escalabilidade (adicionar OSDs), tolerância a falhas (réplicas/self-healing), consistência forte.

## JuiceFS

- **O que é:** sistema de arquivos distribuído **open source** (Apache 2.0), **compatível com POSIX**, feito para a nuvem.
- **Arquitetura em duas partes separadas:**
  - **dados** → guardados em um **armazenamento de objetos** (S3, MinIO, Azure Blob, Google Cloud Storage, inclusive o próprio Ceph), divididos em *chunks/blocos*;
  - **metadados** → num **motor de metadados** à escolha (Redis, MySQL/PostgreSQL, TiKV, SQLite...).
- **Uso:** o cliente **monta** o volume (via **FUSE**) e os programas o enxergam como uma pasta local. Também oferece acesso compatível com HDFS (big data), um gateway S3 e um driver CSI para Kubernetes.
- **Recursos:** cache local no cliente, compressão, criptografia.
- **Relação com a aula:** é o exemplo clássico de **montagem**; separar metadados e dados é a resposta dele para **escalabilidade**; o **cache** levanta a questão de **consistência**.

## Storj

- **O que é:** **armazenamento em nuvem descentralizado**, de objetos e **compatível com S3**, mantido pela Storj Labs.
- **Como funciona:**
  1. o arquivo é **criptografado no cliente** (só o dono tem a chave);
  2. é dividido em segmentos e codificado com **erasure coding** (Reed-Solomon): basta uma parte das peças para reconstruir o arquivo;
  3. as peças vão para **milhares de *storage nodes*** independentes, operados por pessoas e empresas no mundo todo, que são **pagos** pelo espaço e banda (token STORJ);
  4. os **satélites** coordenam metadados, auditorias dos nós, reparo e pagamento.
- **Arquitetura:** **descentralizada/P2P** para os dados, com coordenação pelos satélites, o que lembra os **superpeers** da Aula 02.
- **Relação com a aula:** segurança (criptografia de ponta a ponta), tolerância a falhas (erasure coding e reparo automático quando nós somem), escalabilidade (qualquer um pode oferecer disco).

## Kertish-dfs

- **O que é:** projeto **open source** menor, escrito em **Go**, que se apresenta como um sistema de arquivos distribuído **simples e escalável** para guardar e servir uma **grande quantidade de arquivos** (repositório no GitHub: `freakmaxi/kertish-dfs`).
- **Arquitetura (segundo o README do projeto):** três tipos de nó:
  - **Manager node**: *"responsável pela sincronização e harmonia dos data nodes de cada cluster"*; cuida de reserva de espaço, indexação, saúde do cluster e das operações de verificação/reparo;
  - **Head node(s)**: ponto de acesso dos clientes; fazem **leitura, escrita, exclusão, cópia, movimentação e junção (merge)** de arquivos. Escalam horizontalmente e podem ficar atrás de um balanceador de carga;
  - **Data nodes**: guardam os **pedaços (chunks)** dos arquivos e os servem o mais rápido possível.
- **Dependências externas:** **MongoDB** (metadados e índices), **Redis** (armazenamento compartilhado de dados/sessão) e um **servidor de travas (Locking-Center)** para **lock distribuído**.
- **Replicação:** em cada cluster de data nodes, um é o **mestre** (recebe todas as escritas e exclusões) e os outros são **escravos** com cópias idênticas. **As leituras são balanceadas entre os escravos**, o que favorece ambientes com muita leitura.
- **Acesso:** **API REST/HTTP** pelo head node e duas ferramentas de linha de comando: `krtfs` (operações de arquivo) e `krtadm` (administração do cluster). Não há montagem via FUSE.
- **Relação com a aula:**
  - separa **metadados** (MongoDB, head) de **dados** (data nodes);
  - a **trava distribuída** garante **escrita exclusiva**;
  - **escrever no mestre e ler das réplicas** é exatamente a regra *"leitura compartilhada, escrita exclusiva"* do slide de consistência;
  - adicionar head/data nodes é a resposta dele para **escalabilidade**.

> Fonte: README de `github.com/freakmaxi/kertish-dfs` (consultado em 01/10/2026). Em versões recentes o projeto aparece com o nome **Kertish-DOS**.

## Comparativo

| | Ceph | JuiceFS | Storj | Kertish-dfs |
|---|---|---|---|---|
| Modelo | cluster próprio (on-premise/nuvem privada) | camada de arquivos **sobre** um object storage | rede **descentralizada** global | cluster próprio, simples |
| Interface | objeto (S3), bloco (RBD), arquivo (CephFS) | arquivo **POSIX** (FUSE), HDFS, S3 | objeto (**S3**) | API REST + CLI (`krtfs`, `krtadm`) |
| Metadados | MON/MDS + **CRUSH** (sem tabela central) | motor externo (Redis, SQL, TiKV) | satélites | MongoDB (via head/manager) |
| Tolerância a falhas | replicação / erasure coding, self-healing | herdada do object storage + do motor de metadados | erasure coding + reparo | mestre + réplicas escravas por cluster |
| Destaque | padrão de mercado, muito completo | fácil de montar, cloud-native | criptografia e descentralização | simplicidade |

## Pontos extras: cluster com 3 nós

O caminho mais curto e documentado costuma ser **Ceph com `cephadm`** (ou **MicroCeph**, do Ubuntu, que é ainda mais simples) em **3 VMs**. Dá para aproveitar a **Rede Interna** do VirtualBox de SOA.

Roteiro geral (siga a documentação oficial da versão que for instalar):
1. Três VMs (ex.: `ceph1`, `ceph2`, `ceph3`), cada uma com **um disco extra vazio** para virar OSD, todas na mesma rede e com hostnames resolvíveis.
2. No primeiro nó: `cephadm bootstrap --mon-ip <IP-do-ceph1>`.
3. Distribuir a chave SSH do cluster e adicionar os outros nós: `ceph orch host add ceph2 <IP>` (idem para o ceph3).
4. Criar os OSDs nos discos livres: `ceph orch apply osd --all-available-devices`.
5. Conferir: `ceph status` deve mostrar **3 hosts, 3 OSDs** e `HEALTH_OK`.
6. **Demonstrar tolerância a falhas:** grave um arquivo (CephFS montado ou objeto via `rados`), desligue uma VM e mostre que o dado continua acessível e que o cluster se recupera.

Alternativa mais leve: **JuiceFS** com **MinIO distribuído** em 3 nós como object storage e **Redis** para os metadados, montando o volume nos três.
