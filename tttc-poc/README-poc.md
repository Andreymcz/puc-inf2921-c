# Talk to the City — PoC TRL 3 (Ollama Local)

PoC para rodar o Talk to the City localmente sem dependências de cloud.
Sem OpenAI, sem Firebase, sem GCS, sem PubSub.
Usa o fork `tttc-light-js-ollama` com Ollama como backend LLM.

---

## Pré-requisitos

| Ferramenta | Versão mínima | Como instalar |
|------------|--------------|---------------|
| Git | 2.x | `sudo apt install git` / brew / site oficial |
| Docker Engine | 24.x | https://docs.docker.com/engine/install/ |
| Docker Compose plugin | 2.x | `sudo apt install docker-compose-plugin` |

> **Nota:** O Docker Compose **plugin** (`docker compose`) é necessário — o binário legado `docker-compose` (v1) não é suportado. Verifique com `docker compose version`.

> **Nota:** `uv`, Python e Node.js **não são necessários** na máquina host — tudo roda dentro dos containers Docker.

---

## Setup (primeira vez ou nova máquina)

```bash
# 1. Clonar o repo com o submodule do fork incluído
git clone --recurse-submodules https://git.tecgraf.puc-rio.br/arodrigues/inf2921-grupo-c.git

# Se já tiver o repo clonado sem o submodule:
git submodule update --init

# 2. Entrar no diretório da PoC
cd inf2921-grupo-c/tttc-poc
```

---

## Executar

### 1. Build e subir os containers

```bash
# Dentro de tttc-poc/
docker compose build          # ~5 min na primeira vez (baixa imagens base)
docker compose up -d          # sobe em background
```

Aguarde todos os serviços ficarem `Up`:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### 2. Baixar o modelo LLM (apenas na primeira vez)

```bash
docker exec tttc-poc-ollama-1 ollama pull llama3.2
```

> Isso baixa ~2 GB. O modelo fica salvo no volume `ollama-models` e não precisa ser baixado novamente em próximas execuções.

### 3. Abrir a interface

```
http://localhost:3000
```

### 4. Fazer upload do CSV de teste

Use o arquivo `data/sample-gavealab.csv` (25 respostas qualitativas sobre desafios urbanos na Gávea).

---

## Parar os containers

```bash
docker compose down          # para e remove containers (volumes preservados)
docker compose down -v       # para, remove containers E volumes (apaga modelo baixado)
```

---

## Estrutura

```
tttc-poc/
  tttc-light-js-ollama/       # Fork clonado como git submodule
  data/
    sample-gavealab.csv       # CSV de teste — 25 respostas GaveaLab
  patches/
    express-server/src/
      Firebase.ts             # Stub local (sem firebase-admin)
      storage.ts              # Stub local (sem GCS)
      types/context.ts        # Validação Zod relaxada para PoC
  Dockerfile.express-poc      # Build do express-server com patches aplicados
  Dockerfile.nextclient-poc   # Build do next-client com NEXT_PUBLIC_FIREBASE_* embutidos
  docker-compose.yml          # Orquestração: ollama, redis, pyserver, express-server, next-client
  .env.poc                    # Variáveis de ambiente para modo PoC (sem secrets reais)
  README-poc.md               # Este arquivo
```

---

## Serviços

| Container | Porta | Função |
|-----------|-------|--------|
| `tttc-poc-ollama-1` | 11434 | Servidor Ollama — backend LLM local |
| `tttc-poc-redis-1` | 6379 | Fila BullMQ para jobs de pipeline |
| `tttc-poc-pyserver-1` | 8000 | Pipeline Python (clustering + summarization via Ollama) |
| `tttc-poc-express-server-1` | 8080 | API Node.js — orquestra jobs, salva relatórios localmente |
| `tttc-poc-next-client-1` | 3000 | Frontend Next.js |

---

## Fork (git submodule)

| Campo | Valor |
|-------|-------|
| Repositório | https://github.com/Diegorb1329/tttc-light-js-ollama |
| Commit fixado | `1ddb59d` — "Changing qwen for llama3 and handling json parsing errors" |
| Caminho | `tttc-poc/tttc-light-js-ollama/` |

---

## Variáveis de ambiente (`.env.poc`)

| Variável | Serviço | Valor PoC | Função |
|----------|---------|-----------|--------|
| `USE_OLLAMA` | pyserver | `true` | Ativa Ollama como backend LLM |
| `OLLAMA_BASE_URL` | pyserver | `http://ollama:11434` | URL do container Ollama |
| `OLLAMA_DEFAULT_MODEL` | pyserver | `llama3.2:latest` | Modelo padrão |
| `USE_LOCAL_STORAGE` | express-server | `true` | Bypass de Firebase/GCS |
| `OPENAI_API_KEY` | express-server | `local-ollama-no-key-needed` | Satisfaz validação Zod; não usado em modo Ollama |
| `PYSERVER_URL` | express-server | `http://pyserver:8000` | URL do pipeline LLM |
| `CLIENT_BASE_URL` | express-server | `http://localhost:3000` | URL do frontend para CORS |
| `REDIS_URL` | express-server | `redis://redis:6379` | Fila BullMQ |
| `NODE_ENV` | express-server | `development` | Modo de operação |
| `PIPELINE_EXPRESS_URL` | next-client | `http://express-server:8080` | URL da API |
| `NEXT_PUBLIC_FIREBASE_*` | next-client (build) | stubs | Embutidos no bundle — auth não usada em PoC |

---

## Dados de teste

`data/sample-gavealab.csv` contém 25 respostas qualitativas baseadas no diagnóstico real do GaveaLab (2023), cobrindo 4+ temas distintos (segurança, saúde, infraestrutura, participação). Formato: `id,comment,territory`.

---

## Notas de execução

- Modelo: `llama3.2:latest`
- Primeira execução: ~2 min para baixar o modelo (~2 GB)
- Execuções seguintes: modelo já em cache no volume `ollama-models`
- Relatórios salvos em `/tmp/poc-reports/` dentro do container `express-server`
