# Talk to the City — PoC TRL 3 (Ollama Local)

PoC para rodar o Talk to the City localmente sem dependências de cloud (sem OpenAI, Firebase, GCS, PubSub). Usa o fork `tttc-light-js-ollama` com Ollama como backend LLM.

## Estrutura

```
tttc-poc/
  tttc-light-js-ollama/   # Fork clonado (ver commit abaixo)
  data/
    sample-gavealab.csv   # CSV de teste com dados do GaveaLab
  scripts/                # (a criar) adaptador multi-formato
  docker-compose.yml      # (a criar) orquestração dos serviços
  .env.poc                # (a criar) variáveis de ambiente para modo PoC
  README-poc.md           # Este arquivo
```

## Fork (git submodule)

| Campo | Valor |
|-------|-------|
| Repositório | https://github.com/Diegorb1329/tttc-light-js-ollama |
| Commit fixado | `1ddb59d` — "Changing qwen for llama3 and handling json parsing errors" |
| Caminho | `tttc-poc/tttc-light-js-ollama/` |
| Adicionado como | git submodule (ver `.gitmodules` na raiz do repo) |

## Setup (primeira vez ou nova máquina)

```bash
# Clonar o repo principal com o submodule do fork incluído
git clone --recurse-submodules <url-do-repo>

# Se já tiver o repo clonado sem o submodule:
git submodule update --init
```

## Como executar (após concluir todos os steps)

```bash
# 1. Entrar no diretório da PoC
cd tttc-poc

# 2. Subir os containers
docker compose up

# 3. Baixar o modelo LLM (primeira vez)
docker exec tttc-poc-ollama-1 ollama pull llama3

# 4. Acessar a interface
open http://localhost:3000

# 5. Carregar o CSV de teste
# Usar tttc-poc/data/sample-gavealab.csv
```

## Variáveis de ambiente (`.env.poc`)

| Variável | Serviço | Valor PoC | Função |
|----------|---------|-----------|--------|
| `USE_OLLAMA` | pyserver | `true` | Ativa Ollama como backend LLM |
| `OLLAMA_BASE_URL` | pyserver | `http://ollama:11434` | URL do container Ollama |
| `OLLAMA_DEFAULT_MODEL` | pyserver | `llama3.2:latest` | Modelo padrão |
| `USE_LOCAL_STORAGE` | express-server | `true` | Bypass de Firebase/GCS — salva relatórios localmente |
| `OPENAI_API_KEY` | express-server | `local-ollama-no-key-needed` | Satisfaz validação Zod; não é usada pelo pyserver em modo Ollama |
| `PYSERVER_URL` | express-server | `http://pyserver:8000` | URL do pipeline LLM |
| `CLIENT_BASE_URL` | express-server | `http://localhost:3000` | URL do frontend para CORS |
| `REDIS_URL` | express-server | `redis://redis:6379` | Fila BullMQ |
| `NODE_ENV` | express-server | `development` | Modo de operação |
| `PIPELINE_EXPRESS_URL` | next-client | `http://express-server:8080` | URL da API para submissão de CSVs |
| `NEXT_PUBLIC_FIREBASE_*` | next-client | stubs | Firebase de cliente desativado no modo PoC |

**Patches PoC** (`tttc-poc/patches/`): substituem `Firebase.ts` e `storage.ts` no express-server por implementações locais (sem firebase-admin nem GCS). Aplicados via Docker volume no Step 3.

## Dados de teste

`data/sample-gavealab.csv` contém respostas qualitativas baseadas no diagnóstico real do GaveaLab (2023), simulando uma consulta sobre desafios urbanos e tecnologia na Gávea.

## Notas de execução

*(a preencher após o Step 5 — tempo de processamento, modelo usado, resultado observado)*
