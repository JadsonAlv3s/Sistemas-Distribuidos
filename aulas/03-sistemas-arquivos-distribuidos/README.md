# Aula 03: Sistemas de arquivos distribuídos

> Slides: Aula03.pdf (Tadeu Ferreira Oliveira, 2024)

Mais uma vez, a ideia de SD como **uma interface única para vários equipamentos**, agora aplicada a arquivos.

## 1. Sistema de arquivos **de rede** × **distribuído**

| | **De rede** (ex.: NFS, compartilhamento SMB do Windows) | **Distribuído** (ex.: Ceph, HDFS, JuiceFS) |
|---|---|---|
| Onde ficam os arquivos | **cada arquivo está em um servidor** | **vários arquivos espalhados em vários servidores** (um arquivo pode estar em pedaços e réplicas) |
| O usuário precisa saber | **o nome do servidor** (`\\servidor\pasta`, `servidor:/export`) | **nada sobre a localização**: acessa **como se fosse local** |
| Transparência | baixa | alta |

## 2. Montagem

- Conceito **comum no mundo Unix**: **um novo sistema de arquivos precisa ser montado** num diretório da árvore (o *ponto de montagem*).
- **Depois de montado**, um arquivo que está na rede **pode ser usado como um arquivo local**: os programas usam `open/read/write` normalmente.

```bash
sudo mount -t nfs servidor:/dados /mnt/dados   # monta um compartilhamento NFS
ls /mnt/dados                                  # parece uma pasta local
```

(Ligação com SOA: é o mesmo conceito de *ponto de montagem* do `lsblk` e do `df -h`.)

## 3. As 5 características importantes

### 3.1 Transparência
- Cada arquivo pode estar **total ou parcialmente** em **um ou mais servidores**.
- O usuário **não deve saber** onde o arquivo está fisicamente.
- Para isso, é preciso um **serviço de nomeação independente da localização**: o nome do arquivo não pode conter o servidor (`/projetos/relatorio.pdf`, e não `servidor3:/disco2/relatorio.pdf`). Assim o arquivo pode **mudar de servidor** sem mudar de nome.

### 3.2 Escalabilidade
- **Novos clientes** não podem atrapalhar o funcionamento normal.
- **Novos servidores** devem ser fáceis de adicionar, conforme a necessidade.
- Arquivos concentrados em **poucos locais** viram **gargalo**.

### 3.3 Segurança
- **Permissões distribuídas:** quem tem acesso a cada arquivo, em cada servidor.
- Uma **base de usuários centralizada** pode virar **gargalo** (e ponto único de falha).
- Uma **base distribuída** pode ser mais adequada.

### 3.4 Tolerância a falhas
Perguntas que o sistema precisa responder:
- O que ocorre se um servidor falhar? (Normalmente há **réplicas** em outros servidores.)
- Como **descobrir** que um servidor falhou? (Ex.: *heartbeats*, ou timeouts.)
- Se um cliente **já tinha aberto** um arquivo e o servidor caiu, o que fazer? (Reabrir em outra réplica? Repetir a operação?)
- **Requisições idempotentes**: **várias requisições iguais geram um único efeito**. Se o cliente não sabe se o pedido chegou, ele **repete sem medo**.

| Idempotente ✅ | Não idempotente ❌ |
|---|---|
| "grave estes bytes **na posição 100**" | "**acrescente** estes bytes no fim" (append) |
| "defina o saldo **como** 50" | "**some** 10 ao saldo" |
| ler um bloco, apagar um arquivo pelo nome | criar um arquivo novo com nome sequencial |

Demonstração: [`idempotencia.py`](idempotencia.py) simula uma resposta perdida seguida de reenvio.

### 3.5 Consistência
- Como funciona o **cache**? Cada cliente pode ter cópias locais, e **cache distribuído é complexo** (uma cópia pode ficar desatualizada).
- O que acontece se alguém abrir um arquivo e **outro cliente** também precisar abri-lo?
- Regra clássica (o mesmo princípio de **leitores-escritores**):
  - **leitura** pode ser **compartilhada** (vários leitores ao mesmo tempo);
  - **escrita** deve ser **exclusiva** (um escritor, ninguém mais lendo ou escrevendo).

Ligação com a Aula 01: isso evita a **condição de corrida** entre clientes de máquinas diferentes. É a **exclusão mútua** em escala de rede.

---

## Atividade do slide

Pesquisar e descrever **Kertish-dfs, JuiceFS, Storj e Ceph**: está em [`atividade-pesquisa.md`](atividade-pesquisa.md), com uma tabela comparativa e um roteiro para o cluster de 3 nós dos pontos extras.

## Exercícios

1. Qual a diferença entre sistema de arquivos de rede e distribuído? Dê um exemplo de cada.
2. O que é montagem e por que ela é importante para a transparência?
3. Por que a nomeação precisa ser independente da localização?
4. Dê um exemplo de gargalo de escalabilidade num sistema de arquivos.
5. Por que uma base de usuários centralizada é um risco?
6. O que é uma requisição idempotente? Classifique: (a) `write(arquivo, offset=0, dados)`; (b) `append(arquivo, dados)`; (c) `delete("a.txt")`; (d) `incrementar_contador()`.
7. Por que a idempotência ajuda na tolerância a falhas?
8. Dois clientes abrem o mesmo arquivo. Em quais casos podem fazer isso ao mesmo tempo?
9. Qual o problema de cada cliente manter cache do arquivo?
10. Relacione a regra "leitura compartilhada, escrita exclusiva" com a condição de corrida da Aula 01.

<details><summary><b>Respostas</b></summary>

1. De rede: cada arquivo num servidor e o usuário precisa saber qual (NFS, SMB). Distribuído: arquivos espalhados (e às vezes fragmentados/replicados) em vários servidores, acessados como locais, sem saber onde estão (Ceph, HDFS, JuiceFS).
2. Anexar um sistema de arquivos (inclusive remoto) a um diretório da árvore local. Depois disso os programas o usam com as operações normais de arquivo, sem saber que é remoto.
3. Para que o arquivo possa mudar de servidor (balanceamento, falha, novo servidor) sem mudar de nome e sem quebrar quem o usa. É isso que dá a transparência de localização.
4. Um único servidor guardando os arquivos mais acessados (ou todos os metadados): todo cliente passa por ele, e ele satura.
5. Toda autenticação/consulta de permissão passa por ela: vira gargalo e ponto único de falha.
6. (a) idempotente; (b) não (repetir duplica os dados); (c) idempotente (o efeito final é "não existe a.txt"; a 2ª chamada pode só dar erro "não encontrado"); (d) não.
7. Numa falha, o cliente não sabe se o pedido foi executado e só a resposta se perdeu. Se a operação é idempotente, ele simplesmente repete, sem risco de duplicar o efeito.
8. Se os dois só leem, podem abrir juntos. Se algum vai escrever, a escrita é exclusiva.
9. As cópias podem ficar desatualizadas (um cliente escreve, outro continua lendo a versão velha do cache). É preciso invalidar/atualizar caches, o que é complexo num ambiente distribuído.
10. A condição de corrida acontece quando processos leem e escrevem o mesmo dado e o resultado depende da ordem. Leituras simultâneas não alteram nada (seguras); escrita exclusiva é a exclusão mútua aplicada aos arquivos.
</details>
