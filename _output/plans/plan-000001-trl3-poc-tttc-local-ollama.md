# Plan 000001 | FEATURE-X | 2026-05-24 00:58 UTC | TRL 3 PoC — Talk to the City local (Ollama) | Review: Light
plan_format_version: 1
source: advisory-000004

## User Brief

PoC TRL 3: Talk to the City rodando localmente com Ollama, sem dependências de cloud. Stack simplificada para prova de conceito: Next.js frontend + Express backend + pipeline worker com Ollama local + Docker Compose com 3 serviços. Sem auth, sem storage persistente, sem fila de jobs. Input: CSV com respostas qualitativas. Output: clusters e sumários gerados localmente, visualização interativa no browser. Dados de teste do GaveaLab.

## Agent Interpretation

**Problem:** A equipe quer validar que o Talk to the City (tttc-light-js) consegue produzir análises de respostas qualitativas usando apenas infraestrutura local, sem nenhuma dependência de APIs de nuvem (OpenAI, Firebase, GCS, Pub/Sub), demonstrando a viabilidade técnica para uso pelo GaveaLab.

**Approach:** Usar o fork `tttc-light-js-ollama` como base (já resolve a dependência de OpenAI), desativar auth/storage/fila por variáveis de ambiente, e orquestrar os 3 serviços principais (frontend, backend, Ollama) com um Docker Compose simplificado. A PoC termina quando um CSV de teste gera uma visualização interativa no browser usando apenas recursos locais.

**Alternatives rejected:**
- Modificar o repo principal (AIObjectives/tttc-light-js): exigiria substituir Firebase + GCS + PubSub com código novo — escopo de MVP, não PoC.
- Usar apenas o pipeline worker CLI sem frontend: não demonstra o valor visual da ferramenta para stakeholders do GaveaLab.

## Files

- `tttc-poc/` — novo diretório raiz da PoC (fora do repo kb-qa, ou subdir separado)
- `tttc-poc/docker-compose.yml` — create
- `tttc-poc/.env.poc` — create (variáveis de ambiente para modo PoC)
- `tttc-poc/data/sample-gavealab.csv` — create (dados de teste)
- `tttc-poc/README-poc.md` — create (instruções de execução)

> **Nota:** a PoC é um projeto separado que usa o fork tttc-light-js-ollama como dependência externa (git clone), não modifica o repo kb-qa.

## Best Practices

- Isolamento por Docker Compose — nenhuma dependência de sistema do host além de Docker e Git
- `.env.poc` versionado no repo PoC (sem secrets reais — só flags de modo dev)
- CSV de teste com ≥20 respostas para acionar clustering LLM de forma significativa
- Volumes nomeados para o modelo Ollama (evita re-download a cada `docker compose up`)

## Design Decisions

**User-visible impact:** Stakeholders do GaveaLab poderão abrir `http://localhost:3000` e ver uma visualização interativa de clusters de opiniões gerada a partir de um CSV local, sem internet.

**Trade-offs accepted:** A PoC não tem auth, persistência real, nem fila de jobs. Reiniciar os containers apaga o estado. Isso é aceitável para TRL 3 — o objetivo é demonstrar o pipeline, não operar em produção.

**Metacommunication impact:** N/A — esta PoC não altera o sistema kb-qa nem sua interface com o usuário.

---

## Steps

### Step 1: Clonar e configurar o fork tttc-light-js-ollama

Fazer o clone do fork `https://github.com/Diegorb1329/tttc-light-js-ollama` para um diretório `tttc-poc/` (fora do diretório `inf2921-grupo-c/`, ou como subdiretório isolado acordado pelo time). Verificar que o fork tem branch principal funcional e documentar a versão/commit clonado no `README-poc.md`.

- **Files**: `tttc-poc/` (create — via git clone), `tttc-poc/README-poc.md` (create)
- **References**: N/A
- **Depends on**: none
- **Verify**: `git log --oneline -5` no diretório clonado retorna commits recentes do fork
- **Tests**: N/A
- **Docs**: Anotar no README-poc.md o commit hash clonado e a data
- **Traces**: N/A
- [x] Done

### Step 2: Criar arquivo `.env.poc` desativando serviços de nuvem

Criar `tttc-poc/.env.poc` com variáveis de ambiente que colocam todos os serviços em modo local/mock:
- `OPENAI_API_KEY` apontando para a URL do Ollama local (ex: `http://ollama:11434/v1`)
- `OPENAI_MODEL` = `mistral` (ou outro modelo disponível no Ollama)
- Firebase desativado (variável vazia ou flag `SKIP_AUTH=true` se o fork suportar)
- GCS desativado (flag `USE_LOCAL_STORAGE=true` ou equivalente no fork)
- PubSub desativado (flag `USE_LOCAL_QUEUE=true` ou equivalente no fork)
- `PIPELINE_EXPRESS_URL=http://express-server:8080`

Inspecionar o código do fork em `express-server/` e `pipeline-worker/` para identificar os nomes exatos das variáveis antes de escrever o arquivo.

- **Files**: `tttc-poc/.env.poc` (create)
- **References**: N/A
- **Depends on**: Step 1
- **Verify**: O arquivo `.env.poc` existe e tem todas as variáveis necessárias identificadas no código do fork
- **Tests**: N/A
- **Docs**: Documentar cada variável no README-poc.md com sua função
- **Traces**: N/A
- [ ] Done

### Step 3: Criar `docker-compose.yml` simplificado para PoC

Criar `tttc-poc/docker-compose.yml` com 3 serviços:

```yaml
services:
  ollama:
    image: ollama/ollama
    ports: ["11434:11434"]
    volumes: ["ollama-models:/root/.ollama"]

  express-server:
    build: ./express-server
    env_file: .env.poc
    ports: ["8080:8080"]
    depends_on: [ollama]

  next-client:
    build: ./next-client
    env_file: .env.poc
    ports: ["3000:3000"]
    depends_on: [express-server]

volumes:
  ollama-models:
```

Adaptar os nomes dos diretórios de build conforme a estrutura real do fork clonado no Step 1. Remover serviços desnecessários para PoC (Redis, worker separado se integrado ao express-server no fork).

- **Files**: `tttc-poc/docker-compose.yml` (create)
- **References**: N/A
- **Depends on**: Step 1, Step 2
- **Verify**: `docker compose config` no diretório `tttc-poc/` valida o arquivo sem erros
- **Tests**: N/A
- **Docs**: N/A
- **Traces**: N/A
- [ ] Done

### Step 4: Criar dados de teste do GaveaLab + adaptador multi-formato (PoC)

Este step tem duas partes:

**4a — CSV de teste manual**
Criar `tttc-poc/data/sample-gavealab.csv` com ≥25 respostas qualitativas fictícias mas realistas, simulando uma consulta sobre um tema relevante ao GaveaLab (ex: "Quais são os principais desafios urbanos do bairro da Gávea que a tecnologia poderia ajudar a resolver?"). O CSV deve seguir o formato esperado pelo fork (`id`, `comment`, opcionalmente `interview`) e cobrir ≥4 temas distintos para clustering significativo.

**4b — Script adaptador multi-formato via LLM (PoC do plugin)**
Criar `tttc-poc/scripts/adapt_to_tttc.py` — script Python CLI que usa o Ollama local para converter qualquer arquivo de entrada no formato CSV do T3C:

```
python adapt_to_tttc.py <arquivo_entrada> --output data/output.csv
```

Formatos suportados na PoC: CSV (colunas arbitrárias), XLSX, JSON, TXT simples.

O script deve:
1. Detectar o formato do arquivo de entrada
2. Enviar uma amostra (primeiras 10 linhas/itens) ao Ollama com prompt: *"Identifique quais campos contêm respostas qualitativas de pesquisa. Retorne um JSON com `id_field` e `comment_field`."*
3. Usar os campos identificados para gerar o CSV normalizado `id,comment`
4. Para arquivos TXT/transcrições: segmentar por parágrafo e atribuir IDs sequenciais

**Dependências Python:** `pandas`, `openpyxl`, `requests` (chamada HTTP ao Ollama).

Este script é o embrião do plugin explorado em advisory-000002 (multi-format data ingestion).

- **Files**: `tttc-poc/data/sample-gavealab.csv` (create), `tttc-poc/scripts/adapt_to_tttc.py` (create), `tttc-poc/scripts/requirements.txt` (create)
- **References**: N/A
- **Depends on**: Step 1 (formato esperado pelo fork), Step 3 (Ollama disponível no Compose)
- **Verify**: (a) CSV manual tem cabeçalho correto e ≥25 linhas cobrindo ≥4 temas; (b) `python adapt_to_tttc.py sample-gavealab.csv` retorna CSV normalizado sem erro; (c) testar com pelo menos 2 formatos distintos (ex: XLSX e JSON)
- **Tests**: N/A (PoC)
- **Docs**: Documentar uso do adaptador no README-poc.md com exemplos de cada formato suportado
- **Traces**: N/A
- [ ] Done

### Step 5: Baixar modelo Ollama e executar a PoC end-to-end

Com os containers rodando (`docker compose up`):

1. Baixar o modelo LLM no container Ollama: `docker exec tttc-poc-ollama-1 ollama pull mistral`
2. Aguardar o download completar (pode levar 5-10 minutos na primeira vez)
3. Submeter o CSV de teste via interface web em `http://localhost:3000` ou via API do express-server
4. Aguardar o pipeline processar (clustering + summarization via Ollama)
5. Verificar a visualização interativa no browser

Documentar no README-poc.md o tempo de processamento observado e o modelo usado.

- **Files**: `tttc-poc/README-poc.md` (modify — adicionar resultados)
- **References**: N/A
- **Depends on**: Steps 1–4
- **Verify**: Browser em `http://localhost:3000` exibe visualização interativa com clusters identificados a partir do CSV de teste, sem erros de serviços externos
- **Tests**: N/A
- **Docs**: Capturar screenshot ou descrição da visualização no README-poc.md
- **Traces**: N/A
- [ ] Done

---

## Outcomes

- Diretório `tttc-poc/` com Docker Compose funcional para rodar T3C localmente
- CSV de teste com dados simulados do GaveaLab produzindo visualização real
- README-poc.md documentando como reproduzir a PoC
- Validação técnica de que o pipeline funciona 100% local (sem internet após o `docker pull` inicial)
- Base para extensão futura: step `kb_qa_enrich`, novos inputs, integração com datasets abertos

## Smoke
false

---

## Review Log (Light)

**Complexity gate:** 5 steps, ~5 files → Light depth.

| Perspective | Status | Note |
|-------------|--------|------|
| SEC | Adopted | `.env.poc` sem secrets reais; PoC air-gapped após setup — risco mínimo |
| ARCH | Adopted | Fork isola LLM no Ollama; Docker Compose mantém dependências explícitas |
| OPS | Adopted | Volume nomeado para modelos Ollama evita re-download; PoC stateless por design |
| DX | Deferred | Forks podem divergir do upstream — documentar commit hash no Step 1 mitiga o risco de reprodutibilidade futura |

**Execution Metrics:**

| Metric | Value |
|--------|-------|
| Steps | 5 |
| Files touched | ~5 |
| Review depth | Light |
| Phase 2 deep-dives | 0 |
| Iterations | 1 |
